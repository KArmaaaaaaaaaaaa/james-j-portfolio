#!/usr/bin/env python3
"""Panel para editar el portfolio sin tocar código.

    ./editor.py            -> http://localhost:9130
    ./editor.py --abrir    -> y lo abre en el navegador

Qué hace y qué no: cambia TEXTOS, PRECIOS e IMÁGENES. No rediseña. El diseño
—tamaños, movimiento, dónde va cada sección— sigue viviendo en _build.py y en
_sistema.css, y eso se toca con Claude.

Cómo funciona por dentro: los textos del código son la fuente por defecto y
contenido.json solo guarda LO QUE SE HAYA CAMBIADO. Así, borrar el JSON
devuelve el sitio a su estado original, y si alguien reescribe un texto en el
código, esa anulación se suelta sola y manda el nuevo original.
"""
import ast
import json
import re
import shutil
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parent
FUENTE = RAIZ / "_build.py"
CONTENIDO = RAIZ / "contenido.json"
IMG = RAIZ / "img"
PUERTO = 9130
PUERTO_VISTA = 9131

NOMBRES = {
    "index.html": "Portada",
    "precios.html": "Precios",
    "carta-nfc.html": "Carta en la mesa",
    "ficha-google.html": "Ficha de Google",
    "caso-factura.html": "Un caso",
    "panel-demo.html": "Panel",
}


def correr(orden, tiempo=120):
    r = subprocess.run(orden, cwd=RAIZ, capture_output=True, text=True, timeout=tiempo)
    return r.returncode, (r.stdout + r.stderr).strip()


def clave(original):
    import hashlib
    return hashlib.sha1(original.encode("utf-8")).hexdigest()[:10]


def extraer():
    """Saca del generador todas las llamadas a t(en, es) y v(valor).

    Con el AST y no con expresiones regulares: los textos llevan comillas,
    llaves y HTML dentro, y una regex se los come a medias.
    """
    arbol = ast.parse(FUENTE.read_text(encoding="utf-8"))

    # Dónde acaba cada página: una cadena pertenece a la primera llamada a
    # pagina() que venga por debajo de ella en el fichero.
    cortes = []
    for n in ast.walk(arbol):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "pagina" and n.args
                and isinstance(n.args[0], ast.Constant)):
            cortes.append((n.lineno, n.args[0].value))
    cortes.sort()

    def de_quien(linea):
        for fin, archivo in cortes:
            if linea <= fin:
                return archivo
        return "comun"

    campos, vistos = [], set()
    for n in ast.walk(arbol):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)):
            continue
        if n.func.id == "t" and len(n.args) == 2:
            if not all(isinstance(a, ast.Constant) and isinstance(a.value, str)
                       for a in n.args):
                continue
            en, es = n.args[0].value, n.args[1].value
            k = clave(en)
            if k in vistos:
                continue
            vistos.add(k)
            campos.append({"clave": k, "tipo": "texto", "en": en, "es": es,
                           "pagina": de_quien(n.lineno), "linea": n.lineno})
        elif n.func.id == "v" and len(n.args) == 1:
            a = n.args[0]
            if not (isinstance(a, ast.Constant) and isinstance(a.value, str)):
                continue
            k = clave(a.value)
            if k in vistos:
                continue
            vistos.add(k)
            campos.append({"clave": k, "tipo": "valor", "en": a.value,
                           "es": a.value, "pagina": de_quien(n.lineno),
                           "linea": n.lineno})
    campos.sort(key=lambda c: c["linea"])
    return campos


def guardados():
    if not CONTENIDO.exists():
        return {}
    try:
        return json.loads(CONTENIDO.read_text(encoding="utf-8")).get("textos", {})
    except json.JSONDecodeError:
        return {}


def estado():
    puestos = guardados()
    campos = extraer()
    for c in campos:
        p = puestos.get(c["clave"])
        c["cambiado"] = bool(p)
        c["en_actual"] = (p or {}).get("en") or c["en"]
        c["es_actual"] = (p or {}).get("es") or c["es"]
    imagenes = sorted(f.name for f in IMG.glob("*")
                      if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".svg"))
    # Huecos: sitios del diseño que aceptan una imagen aunque hoy estén
    # dibujados con CSS. Se listan estén llenos o vacíos, porque si no, no
    # habría manera de descubrir que se pueden rellenar.
    huecos = []
    for base, que, nota in [
        ("lamina", "Lámina de la portada",
         "Hoy es cromo dibujado con CSS. Si subes una imagen, ocupa su sitio "
         "con la misma inclinación y la misma sombra. Vertical, y que aguante "
         "un recorte 284×496. Menos de 300 KB."),
    ]:
        actual = next((f.name for f in sorted(IMG.glob(base + ".*"))
                       if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".svg")), None)
        huecos.append({"base": base, "que": que, "nota": nota, "actual": actual})
    paginas = [{"archivo": a, "nombre": NOMBRES.get(a, a)}
               for a in list(NOMBRES) if any(c["pagina"] == a for c in campos)]
    if any(c["pagina"] == "comun" for c in campos):
        paginas.insert(0, {"archivo": "comun", "nombre": "Común (barra y pie)"})
    return {"campos": campos, "imagenes": imagenes, "huecos": huecos,
            "paginas": paginas,
            "cambios": sum(1 for c in campos if c["cambiado"])}


def escribir(cambios):
    """Guarda solo lo que difiere del original. Lo igual no se guarda."""
    originales = {c["clave"]: c for c in extraer()}
    puestos = {}
    for k, val in (cambios or {}).items():
        orig = originales.get(k)
        if not orig:
            continue
        en = (val.get("en") or "").strip()
        es = (val.get("es") or "").strip()
        if en and en != orig["en"]:
            puestos.setdefault(k, {})["en"] = en
        if es and es != orig["es"]:
            puestos.setdefault(k, {})["es"] = es
    if puestos:
        CONTENIDO.write_text(json.dumps({"textos": puestos}, ensure_ascii=False,
                                        indent=2) + "\n", encoding="utf-8")
    elif CONTENIDO.exists():
        CONTENIDO.unlink()
    return len(puestos)


def generar():
    c1, s1 = correr([sys.executable, "_build.py"])
    c2, s2 = correr([sys.executable, "_build.py", "es"])
    return (c1 == 0 and c2 == 0), (s1 + "\n" + s2).strip()


def publicar():
    ok, salida = generar()
    if not ok:
        return False, "No compila, no se publica:\n" + salida
    correr(["git", "add", "-A", "index.html", "precios.html", "carta-nfc.html",
            "ficha-google.html", "caso-factura.html", "panel-demo.html",
            "contenido.json", "img", "_build.py"])
    cod, _ = correr(["git", "diff", "--cached", "--quiet"])
    if cod == 0:
        return False, "No hay nada que publicar: no ha cambiado nada."
    cod, salida = correr(["git", "commit", "-m",
                          "Contenido editado desde el panel"])
    if cod != 0:
        return False, "El commit ha fallado:\n" + salida
    cod, salida = correr(["git", "push", "origin", "main"], tiempo=180)
    if cod != 0:
        return False, "El push ha fallado:\n" + salida
    return True, "Publicado. GitHub Pages tarda un minuto en refrescarlo."


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _responder(self, cuerpo, tipo="application/json", codigo=200):
        if isinstance(cuerpo, str):
            cuerpo = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo + ("; charset=utf-8"
                         if "image" not in tipo else ""))
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _cuerpo(self):
        largo = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(largo) if largo else b""

    def do_GET(self):
        ruta = self.path.split("?")[0]
        if ruta in ("/", "/index.html"):
            return self._responder((RAIZ / "editor.html").read_text(encoding="utf-8"),
                                   "text/html")
        if ruta == "/api/estado":
            return self._responder(json.dumps(estado(), ensure_ascii=False))
        if ruta.startswith("/img/"):
            # Resuelto y comprobado dentro de img/: sin esto, «/img/../../.ssh»
            # saldría de la carpeta.
            destino = (IMG / unquote(ruta[len("/img/"):])).resolve()
            if not str(destino).startswith(str(IMG.resolve()) + "/") or not destino.is_file():
                return self._responder('{"error":"no existe"}', codigo=404)
            tipos = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                     ".png": "image/png", ".webp": "image/webp"}
            return self._responder(destino.read_bytes(),
                                   tipos.get(destino.suffix.lower(), "application/octet-stream"))
        self._responder('{"error":"ruta desconocida"}', codigo=404)

    def do_POST(self):
        ruta = self.path.split("?")[0]
        try:
            if ruta == "/api/guardar":
                n = escribir(json.loads(self._cuerpo() or b"{}").get("cambios"))
                return self._responder(json.dumps({"ok": True, "guardados": n}))
            if ruta == "/api/ver":
                ok, salida = generar()
                return self._responder(json.dumps({"ok": ok, "salida": salida,
                                                   "url": f"http://localhost:{PUERTO_VISTA}/"}))
            if ruta == "/api/publicar":
                ok, mensaje = publicar()
                return self._responder(json.dumps({"ok": ok, "mensaje": mensaje}))
            if ruta.startswith("/api/quitar/"):
                nombre = unquote(ruta[len("/api/quitar/"):])
                if "/" in nombre or ".." in nombre or not nombre:
                    return self._responder('{"error":"nombre no válido"}', codigo=400)
                f = IMG / nombre
                if not f.is_file():
                    return self._responder('{"error":"no existe"}', codigo=404)
                # No se borra: se aparta. Recuperarla es renombrar el fichero.
                f.rename(f.with_suffix(f.suffix + ".apartada"))
                return self._responder(json.dumps({"ok": True}))
            if ruta.startswith("/api/imagen/"):
                nombre = unquote(ruta[len("/api/imagen/"):])
                # Solo un nombre de fichero, jamás una ruta.
                if "/" in nombre or ".." in nombre or not nombre:
                    return self._responder('{"error":"nombre no válido"}', codigo=400)
                destino = IMG / nombre
                # Un hueco puede llegar sin extensión ("lamina"): se le pone
                # .jpg, que es lo que el generador busca con img/lamina.*
                if not destino.suffix:
                    destino = destino.with_suffix(".jpg")
                if destino.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".svg"):
                    return self._responder('{"error":"solo jpg, png o webp"}', codigo=400)
                datos = self._cuerpo()
                if not datos:
                    return self._responder('{"error":"vacío"}', codigo=400)
                if destino.exists():
                    shutil.copy2(destino, destino.with_suffix(destino.suffix + ".anterior"))
                destino.write_bytes(datos)
                return self._responder(json.dumps({"ok": True, "bytes": len(datos)}))
        except Exception as e:
            return self._responder(json.dumps({"ok": False, "error": str(e)}),
                                   codigo=500)
        self._responder('{"error":"ruta desconocida"}', codigo=404)


def main():
    # La vista previa: un servidor estático aparte sobre la carpeta ya generada.
    subprocess.Popen([sys.executable, "-m", "http.server", str(PUERTO_VISTA),
                      "--bind", "127.0.0.1"], cwd=RAIZ,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    servidor = ThreadingHTTPServer(("127.0.0.1", PUERTO), Manejador)
    servidor.daemon_threads = True
    print(f"Panel en http://localhost:{PUERTO}/   (vista previa en :{PUERTO_VISTA})")
    if "--abrir" in sys.argv:
        webbrowser.open(f"http://localhost:{PUERTO}/")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrado.")


if __name__ == "__main__":
    main()
