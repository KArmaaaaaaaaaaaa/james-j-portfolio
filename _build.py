#!/usr/bin/env python3
"""Genera el sitio de James J Projects.

    python3 _build.py          -> inglés (lo que se publica)
    python3 _build.py es       -> castellano, en /es/

Una sola fuente para los dos idiomas: los textos viven en T() y el resto
—estructura, sistema visual, movimiento— se comparte. Se decidió publicar en
inglés el 7/9/2026 de cara a la mudanza a Hamburgo; el castellano se mantiene
generable porque el cliente que hoy paga es un dueño de bar español.

El mundo visual está en _sistema.css y la dirección en
.impeccable/surfaces/index-html.md. Aquí solo va lo que cambia por página.
"""
import pathlib, sys, re

BASE = pathlib.Path(__file__).parent
SISTEMA = (BASE / "_sistema.css").read_text(encoding="utf-8")
IDIOMA = "es" if len(sys.argv) > 1 and sys.argv[1] == "es" else "en"
SALIDA = BASE / "es" if IDIOMA == "es" else BASE

# Las páginas en castellano se escriben en /es/, así que todo lo que no sea
# HTML vive un nivel más arriba.
A = "../" if IDIOMA == "es" else ""
# La lámina de la portada es cromo dibujado con gradientes. Si hay una imagen
# en img/lamina.*, manda ella: así se puede poner una ilustración de verdad
# —un cartel, una lámina de aerografía— sin tocar una línea de código. El
# marco, la inclinación y la sombra dura se quedan: lo que cambia es lo de
# dentro, no la composición.
# Orden explícito, no alfabético: si conviven un lamina.svg y un lamina.jpg
# —pasa al probar—, el alfabeto elegiría el jpg por casualidad. El vector
# manda, que pesa menos y no se pixela.
_ORDEN = (".svg", ".webp", ".png", ".jpg", ".jpeg")
LAMINA = next((n for n in
               (f"lamina{e}" for e in _ORDEN)
               if (BASE / "img" / n).exists()), None)

FUENTES = (BASE / "_fuentes.css").read_text(encoding="utf-8").replace(
    "url(fuentes/", f"url({A}fuentes/")

# ── Menú ───────────────────────────────────────────────────────────────
NAV = [
  ("index.html",        {"en":"Home",           "es":"Inicio"}),
  ("precios.html",      {"en":"Pricing",        "es":"Precios"}),
  ("carta-nfc.html",    {"en":"Menu on the table","es":"Carta en la mesa"}),
  ("ficha-google.html", {"en":"Google profile",  "es":"Ficha de Google"}),
  ("caso-factura.html", {"en":"Case",            "es":"Un caso"}),
  ("panel-demo.html",   {"en":"Dashboard",       "es":"Panel"}),
]

# ── El contenido editable ──────────────────────────────────────────────
# contenido.json NO sustituye a los textos del código: los ANULA. Lo que no
# se haya tocado en el panel sigue saliendo de aquí, así que borrar el JSON
# devuelve el sitio a su estado original y una clave que ya no exista no
# rompe nada. La clave es un hash del texto en inglés: si se reescribe el
# original a mano, la anulación de ese texto se suelta, que es lo correcto —
# el original nuevo manda.
import hashlib, json

TEXTOS = {}
_JSON = BASE / "contenido.json"
if _JSON.exists():
    try:
        TEXTOS = json.loads(_JSON.read_text(encoding="utf-8")).get("textos", {})
    except json.JSONDecodeError as e:
        print(f"  ¡ojo! contenido.json ilegible ({e}); se usa el texto del código")


def clave(original):
    """Clave estable de un texto, para casar código y panel."""
    return hashlib.sha1(original.encode("utf-8")).hexdigest()[:10]


def t(en, es):
    """Un texto en los dos idiomas, con la anulación del panel si la hay."""
    puesto = TEXTOS.get(clave(en))
    if isinstance(puesto, dict):
        en = puesto.get("en") or en
        es = puesto.get("es") or es
    return en if IDIOMA == "en" else es


def v(valor):
    """Un valor igual en los dos idiomas: un precio, una cifra, un plazo."""
    puesto = TEXTOS.get(clave(valor))
    if isinstance(puesto, dict):
        return puesto.get("en") or valor
    return valor

def euros(entero, dec="00"):
    """5574 -> «5,574.00 €» en inglés, «5.574,00 €» en castellano."""
    miles = f"{entero:,}".replace(",", "." if IDIOMA == "es" else ",")
    coma = "," if IDIOMA == "es" else "."
    return f"{miles}{coma}{dec}\u00a0€"

def num(n):
    return f"{n:,}".replace(",", "." if IDIOMA == "es" else ",")

DEMO = "https://sitio-demo-bar.jamesjoelbenavides2004.workers.dev"
CORREO = "jamesjoelbenavides2004@gmail.com"

# ── El movimiento ──────────────────────────────────────────────────────
# Un solo momento de autor por página, no la misma entrada en cada sección:
# lo que sube es la primera línea de cada plate, y el resto llega detrás
# escalonado 60 ms y parando a los seis.
JS = r"""
const obs=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){
  e.target.classList.add('dentro');obs.unobserve(e.target);}},
  {threshold:.14,rootMargin:'0px 0px -8% 0px'});
const cuenta=new Map();
document.querySelectorAll('.sube').forEach(el=>{
  const p=el.parentElement;const n=cuenta.get(p)??0;cuenta.set(p,n+1);
  el.style.transitionDelay=Math.min(n,5)*60+'ms';obs.observe(el);});
/* Red de seguridad: si la pestaña se abre en segundo plano el observador no
   dispara nunca y la página se queda en blanco para siempre. */
setTimeout(()=>document.querySelectorAll('.sube').forEach(el=>el.classList.add('dentro')),2600);

/* Parallax: lo marcado con data-lento avanza a una fracción del scroll, así
   que el nombre a sangre se queda atrás y el contenido pasa por encima. Solo
   transform, en un rAF, y ni se enciende si se pide movimiento reducido. */
const lentos=[...document.querySelectorAll('[data-lento]')];
if(lentos.length&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  let pedido=false;
  const mover=()=>{const y=window.scrollY;
    for(const el of lentos){const f=parseFloat(el.dataset.lento)||0;
      el.style.transform='translate3d(0,'+(y*f).toFixed(1)+'px,0)';}
    pedido=false;};
  addEventListener('scroll',()=>{if(!pedido){pedido=true;requestAnimationFrame(mover);}},
    {passive:true});
  mover();}

/* La barra se aprieta en cuanto se baja: menos chrome delante del contenido. */
const barraEl=document.querySelector('.barra');
if(barraEl){let apretada=false;
  addEventListener('scroll',()=>{const debe=window.scrollY>40;
    if(debe!==apretada){apretada=debe;barraEl.classList.toggle('apretada',debe);}},
    {passive:true});}

const btn=document.getElementById('menuBtn'),panel=document.getElementById('menuPanel');
if(btn&&panel){
  const cerrar=(devolver)=>{
    if(panel.hidden)return;
    btn.setAttribute('aria-expanded','false');panel.hidden=true;
    document.body.classList.remove('menu-abierto');
    if(devolver)btn.focus();};
  const abrir=()=>{
    btn.setAttribute('aria-expanded','true');panel.hidden=false;
    document.body.classList.add('menu-abierto');};
  btn.addEventListener('click',()=>{panel.hidden?abrir():cerrar(false);});
  /* Pulsar una entrada del índice cierra el panel además de navegar: si el
     destino es un ancla de la misma página, la navegación no recarga nada y
     el menú se quedaba abierto tapando justo lo que se acababa de pedir. */
  panel.addEventListener('click',e=>{if(e.target.closest('a'))cerrar(false);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')cerrar(true);});
}
"""

def barra(actual):
    """La barra y el índice. Los enlaces existen UNA vez, en el panel.

    Antes se pintaban dos veces —inline en la barra y otra vez en el panel—,
    que además de repetirse en pantalla se lee dos veces con un lector.
    """
    filas = "".join(
      f'<a href="{h}"{" aria-current=\'page\'" if h == actual else ""}>'
      f'<span class="n">{i:02d}</span><span>{d[IDIOMA]}</span>'
      f'<span class="flecha" aria-hidden="true">→</span></a>'
      for i, (h, d) in enumerate(NAV, 1))
    correo_fila = (
      f'<a href="mailto:{CORREO}"><span class="n">{len(NAV)+1:02d}</span>'
      f'<span>{t("Talk to me","Hablamos")}</span>'
      f'<span class="flecha" aria-hidden="true">→</span></a>')
    return f"""
<nav class="barra" aria-label="{t('Main','Principal')}">
  <a class="marca" href="index.html">James J Projects</a>
  <a class="cta" href="mailto:{CORREO}">{t('Talk to me','Hablamos')}</a>
  <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menuPanel"
    aria-label="{t('Open the index','Abrir el índice')}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
      stroke-linecap="round" aria-hidden="true"><path class="r1" d="M4 8h16"/><path
      class="r2" d="M4 16h16"/></svg>
  </button>
</nav>
<div class="menu-panel" id="menuPanel" hidden>
  <div class="menu-lista">{filas}{correo_fila}</div>
</div>"""


PIE = f"""
<footer class="pie">
  <div class="env">
    <div class="pie-fila">
      <span class="marca-pie">James J Projects</span>
      <span class="spec">{t('Barcelona and Hamburg · remote','Barcelona y Hamburgo · en remoto')}</span>
    </div>
    <p class="nota pie-nota">{t(
      'Hand-built. No template, no framework, no tracking, and nothing at all loaded from a third party — the typefaces are served from here.',
      'Hecho a mano. Sin plantilla, sin framework, sin rastreo y sin nada de terceros: las tipografías se sirven desde aquí.')}</p>
  </div>
</footer>"""

def pagina(archivo, titulo, descripcion, cuerpo, css_extra="", js_extra=""):
    lang = "en" if IDIOMA == "en" else "es"
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preload" href="{A}fuentes/hanken-grotesk-300-600-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{A}fuentes/oswald-400-500-latin.woff2" as="font" type="font/woff2" crossorigin>
<noscript><style>.sube{{opacity:1!important;transform:none!important}}
.titular .linea > i,.firma,.cupo,.acciones{{opacity:1!important;transform:none!important;animation:none!important}}
/* Sin JS nadie pone `.dentro`, y la factura y el embudo son contenido, no
   adorno: se quedarían invisibles para siempre. */
.factura .lin,.factura .sum,.factura .tot,.factura .de{{opacity:1!important;transform:none!important;animation:none!important}}
.embudo .via > i{{transform:scaleX(1)!important;animation:none!important}}</style></noscript>
<style>
{FUENTES}
{SISTEMA}
{CHASIS}
{css_extra}
</style>
</head>
<body>
<a class="saltar" href="#principal">{t('Skip to the content','Saltar al contenido')}</a>
{barra(archivo)}
{cuerpo}
{PIE}
<script>{JS}
{js_extra}</script>
</body>
</html>"""
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / archivo).write_text(html, encoding="utf-8")
    print(f"  {archivo}")

# ── Chasis: barra, menú, pie ───────────────────────────────────────────
CHASIS = """
.barra{position:fixed;z-index:60;top:16px;left:50%;transform:translateX(-50%);
  display:flex;align-items:center;gap:4px;background:rgba(255,255,255,.9);
  backdrop-filter:saturate(180%) blur(16px);border:1px solid var(--hilo);
  padding:7px 8px 7px 18px;max-width:calc(100vw - 32px)}
.barra .marca{font-family:var(--display);font-size:19px;text-transform:uppercase;
  letter-spacing:.01em;color:var(--tinta);text-decoration:none;margin-right:14px;
  white-space:nowrap}
.barra a:not(.marca){font-family:var(--mono);font-size:11px;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:var(--tinta-2);
  text-decoration:none;padding:9px 12px;white-space:nowrap;
  transition:color var(--rapido) var(--curva),background var(--rapido) var(--curva)}
.barra a:not(.marca):hover{color:var(--tinta);background:var(--hueco)}
.barra a[aria-current]{color:var(--tinta);background:var(--hueco)}
.barra .cta{background:var(--tinta)!important;color:var(--papel)!important}
.barra .cta:hover{background:var(--fuego-fondo)!important;color:#fff!important}
.barra{transition:padding var(--rapido) var(--curva),
  background var(--rapido) var(--curva),transform var(--normal) var(--curva)}
.barra.apretada{padding-top:4px;padding-bottom:4px;background:rgba(255,255,255,.96)}
.barra.apretada .marca{font-size:17px}
.barra .marca{transition:font-size var(--rapido) var(--curva)}

/* Un solo índice, el mismo en el móvil y en el Mac.
   Antes la barra enseñaba los seis enlaces Y el botón abría un panel con esos
   mismos seis: la misma lista dos veces en la misma pantalla. Ahora la barra
   lleva marca y llamada, y el índice vive en un único sitio. De paso desaparece
   el problema del móvil de raíz: el panel ya no «tapa» la página, ocupa la
   pantalla entera y tiene una salida que se ve. */
.menu-btn{display:block;background:none;border:0;padding:8px;cursor:pointer;
  color:var(--tinta);position:relative;z-index:60;
  transition:transform var(--micro) var(--curva),color var(--rapido) var(--curva)}
.menu-btn:hover{color:var(--fuego-texto)}
.menu-btn:active{transform:scale(.94)}
.menu-btn svg{width:21px;height:21px;display:block}
.menu-btn svg path{transform-origin:center;
  transition:transform var(--normal) var(--expo)}
.menu-btn[aria-expanded="true"] .r1{transform:translateY(4px) rotate(45deg)}
.menu-btn[aria-expanded="true"] .r2{transform:translateY(-4px) rotate(-45deg)}
@media(hover:none){.menu-btn:hover{color:var(--tinta)}}

/* El índice, a pantalla completa. Papel, no negro: este sitio vive en claro. */
.menu-panel{position:fixed;inset:0;z-index:55;background:var(--papel);
  display:flex;flex-direction:column;justify-content:center;
  padding:96px 6vw 40px;overflow-y:auto;overscroll-behavior:contain;
  animation:panelEntra var(--normal) var(--entrada) both}
.menu-panel[hidden]{display:none}
@keyframes panelEntra{from{opacity:0;clip-path:inset(0 0 100% 0)}
                      to{opacity:1;clip-path:inset(0 0 0 0)}}

/* La cuña cobalto: el mismo plano inclinado que la lámina de la portada. */
.menu-panel::before{content:"";position:absolute;z-index:0;pointer-events:none;
  right:-12vw;top:-10vh;width:46vw;height:120vh;background:var(--cobalto);
  transform:rotate(9deg);opacity:.9}
@media(max-width:860px){.menu-panel::before{right:-38vw;width:76vw;opacity:.86}}

.menu-lista{position:relative;z-index:1;display:grid;
  max-width:var(--ancho);width:100%;margin:0 auto;
  border-top:1px solid var(--tinta)}
.menu-panel a{display:grid;grid-template-columns:auto 1fr auto;gap:20px;
  align-items:baseline;padding:clamp(14px,2.4vh,26px) 4px;
  border-bottom:1px solid var(--tinta);text-decoration:none;color:var(--tinta);
  font-family:var(--display);font-size:clamp(26px,5.4vw,60px);font-weight:500;
  line-height:1;text-transform:uppercase;letter-spacing:-.01em;
  opacity:0;transform:translateY(16px);
  transition:color var(--rapido) var(--curva),
             padding-left var(--rapido) var(--curva)}
.menu-panel:not([hidden]) a{animation:filaEntra 420ms var(--expo) both}
@keyframes filaEntra{to{opacity:1;transform:none}}
.menu-panel a:nth-child(1){animation-delay:60ms}
.menu-panel a:nth-child(2){animation-delay:110ms}
.menu-panel a:nth-child(3){animation-delay:160ms}
.menu-panel a:nth-child(4){animation-delay:210ms}
.menu-panel a:nth-child(5){animation-delay:260ms}
.menu-panel a:nth-child(6){animation-delay:310ms}
.menu-panel a:nth-child(n+7){animation-delay:360ms}
.menu-panel a .n{font-family:var(--mono);font-size:11px;font-weight:600;
  letter-spacing:.16em;color:var(--tinta-3);align-self:center}
.menu-panel a .flecha{font-family:var(--mono);font-size:14px;color:var(--fuego-texto);
  opacity:0;transform:translateX(-8px);align-self:center;
  transition:opacity var(--rapido) var(--curva),
             transform var(--rapido) var(--curva)}
.menu-panel a:hover{color:var(--fuego-texto);padding-left:18px}
.menu-panel a:hover .flecha{opacity:1;transform:none}
.menu-panel a[aria-current]{color:var(--cobalto)}
.menu-panel a[aria-current] .n{color:var(--cobalto)}
@media(hover:none){.menu-panel a:hover{color:var(--tinta);padding-left:4px}
  .menu-panel a:hover .flecha{opacity:1;transform:none}}
/* Con el índice delante el fondo no se mueve: en el móvil, hacer scroll con el
   menú abierto desplazaba la página por detrás. */
body.menu-abierto{overflow:hidden}
@media(prefers-reduced-motion:reduce){
  .menu-panel,.menu-panel a{animation:none;opacity:1;transform:none}}
@media(hover:none){.barra a:not(.marca):hover{background:none;color:var(--tinta-2)}}

.pie{border-top:1px solid var(--tinta);padding:34px 0 54px;margin-top:0}
.pie-fila{display:flex;justify-content:space-between;align-items:baseline;
  gap:20px;flex-wrap:wrap}
.marca-pie{font-family:var(--display);font-size:20px;text-transform:uppercase}
.pie-nota{margin-top:16px}

/* ── El mundo: la pieza cromada, su sombra dura y sus destellos ─────
   Vive en el chasis, no en la portada: si solo aparece en una página no es
   un mundo, es un adorno. En estrecho no se esconde, se muda a la esquina y
   se sale del plano, que es lo que hace una lámina de aerografía. */
.plate{position:relative;overflow:hidden}
.plate > .env{position:relative;z-index:1}
.pieza{position:absolute;z-index:0;pointer-events:none;
  right:-34px;bottom:-42px;width:118px;height:156px;
  transform:rotate(-8deg);box-shadow:16px 16px 0 rgba(0,0,0,.32)}
@media(min-width:1080px){
  .pieza{right:6%;bottom:auto;top:50%;width:184px;height:244px;
    transform:translateY(-50%) rotate(-8deg);
    box-shadow:24px 24px 0 rgba(0,0,0,.32)}}
.pieza .chispa{--chispa:64px;left:52%;top:27%}
/* El margen lateral de una franja solo existe por encima de 1440 px; por
   debajo, un destello al 33% cae sobre el párrafo. Así que por defecto van a
   las esquinas y solo bajan al margen cuando hay margen. */
.plate .chispa.a{--chispa:72px;left:89%;top:7%;bottom:auto}
.plate .chispa.b{--chispa:44px;left:9%;bottom:8%;top:auto}
@media(min-width:1440px){
  .plate .chispa.a{--chispa:104px;left:5%;top:26%}
  .plate .chispa.b{--chispa:60px;left:10%;bottom:20%}}
@media(prefers-reduced-motion:no-preference){
  .plate > .chispa{animation:brillar 3.6s var(--curva) infinite}
  .plate > .chispa.b{animation-delay:1.2s}
  @keyframes brillar{0%,74%,100%{opacity:0;transform:translate(-50%,-50%) scale(.45)}
                     84%{opacity:1;transform:translate(-50%,-50%) scale(1)}}}

/* Pasos numerados y ficha de hechos. Viven aquí y no en el CSS de una
   página porque los usan dos: en caso-factura.html los pasos salían sin
   rejilla y en ficha-google.html los hechos salían sin bordes. */
.pasos{border-top:1px solid var(--tinta);margin-top:12px}
.paso{display:grid;grid-template-columns:44px 1fr;gap:20px;align-items:start;
  padding:26px 0;border-bottom:1px solid var(--tinta)}
.paso .n{font-family:var(--display);font-size:30px;line-height:.9;
  color:var(--tinta-3)}
.paso h3{margin-bottom:8px}
.paso p{font-size:15.5px;color:var(--tinta-2);font-weight:300}
@media(max-width:560px){.paso{grid-template-columns:32px 1fr;gap:14px}}

.hechos{display:grid;grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--hilo-cobalto);margin-top:48px}
.hechos > div{padding:18px 16px 0 0;border-right:1px solid var(--hilo-cobalto)}
.hechos > div:last-child{border-right:0}
.hechos .dato{font-family:var(--display);font-size:clamp(21px,2.8vw,34px);
  line-height:1;text-transform:uppercase;color:#fff;margin-top:9px}
@media(max-width:760px){.hechos{grid-template-columns:1fr 1fr}
  .hechos > div:nth-child(2){border-right:0}
  .hechos > div:nth-child(-n+2){border-bottom:1px solid var(--hilo-cobalto);
    padding-bottom:16px}}

/* La portada: la única que empieza pegada arriba */
.portada{padding:132px 0 0;position:relative}
@media(max-width:760px){.portada{padding-top:104px}}

/* ── La retícula ────────────────────────────────────────────────────
   Cruces de registro, las de una plancha de impresión y las de un HUD de
   mecha. Van en el fondo, sin bloquear el ratón, y son un SVG de 24 bytes
   repetido: ni una petición más, que el sitio no carga nada de fuera. */
.reticula{position:absolute;inset:0;z-index:0;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cpath d='M69 75h12M75 69v12' stroke='%230d0d0f' stroke-opacity='.30' stroke-width='1'/%3E%3C/svg%3E");
  background-repeat:repeat;background-position:center}
.plate .reticula{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cpath d='M69 75h12M75 69v12' stroke='%23ffffff' stroke-opacity='.42' stroke-width='1'/%3E%3C/svg%3E")}
@media(max-width:640px){.reticula{background-size:104px 104px}}

/* ── El nombre, a sangre ────────────────────────────────────────────
   El gesto es el de una portada de disco: el nombre ocupa todo el ancho, se
   sale por los lados y el contenido pasa por encima al bajar. Va detrás de
   todo y en fuego sobre papel, no en negro: este sitio vive en claro. */
.sello{position:relative;z-index:0;pointer-events:none;user-select:none;
  overflow:hidden;line-height:1;margin-top:clamp(52px,9vh,120px);
  margin-bottom:-.2em}
.sello span{display:block;white-space:nowrap;text-align:center;
  font-family:var(--display);font-weight:500;letter-spacing:-.03em;
  font-size:clamp(84px,20.5vw,300px);color:var(--fuego);
  transform:translateY(14%);opacity:0;
  animation:sello 720ms var(--expo) 320ms both;
  will-change:transform}
@keyframes sello{to{transform:translateY(0);opacity:1}}
/* La marca registrada al vuelo, como en las láminas de los ochenta. */
.sello i{font-style:normal;font-size:.2em;vertical-align:super;
  letter-spacing:0;margin-left:.06em}
@media(max-width:760px){.sello{margin-top:44px}}
@media(prefers-reduced-motion:reduce){
  .sello span{animation:none;opacity:1;transform:none}}
"""

# ═══════════════════════════ 1. PORTADA ═══════════════════════════════
CSS_HOME = """
/* La portada pide más presencia que el resto de páginas: es lo primero y a
   veces lo único que alguien mira. Sube solo aquí, no en los h1 del resto. */
.portada .titular{font-size:clamp(40px,9.4vw,132px);letter-spacing:-.015em}
.titular .linea{display:block;overflow:hidden;padding-bottom:.2em}
.titular .linea > i{display:block;font-style:normal;transform:translateY(105%);
  opacity:0;animation:subir 640ms var(--expo) both}
.titular .linea:nth-child(1) > i{animation-delay:60ms}
.titular .linea:nth-child(2) > i{animation-delay:130ms}
.titular .linea:nth-child(3) > i{animation-delay:200ms}
@keyframes subir{to{transform:none;opacity:1}}
.titular .apagado{color:var(--tinta-3)}
.subrayado{position:relative;display:inline-block;line-height:1;font-style:normal}
.subrayado::after{content:"";position:absolute;left:0;right:0;top:1.02em;
  height:.05em;background:var(--fuego);transform:scaleX(0);transform-origin:left;
  animation:trazar 560ms var(--curva) 700ms both}
@keyframes trazar{to{transform:scaleX(1)}}

.firma{margin-top:36px;display:grid;gap:13px;max-width:42rem;
  border-left:2px solid var(--fuego);padding-left:22px;
  animation:aparecer 560ms var(--entrada) 300ms both}
.firma .guia{font-size:clamp(19px,2.1vw,23.5px);line-height:1.5;
  color:var(--tinta-2)}
@keyframes aparecer{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.cupo{display:inline-flex;align-items:center;gap:11px;margin-top:26px;
  font-family:var(--display);font-size:15px;font-weight:500;letter-spacing:.05em;
  text-transform:uppercase;border:1px solid var(--tinta);padding:11px 19px;
  animation:aparecer 560ms var(--entrada) 380ms both;
  transition:transform var(--rapido) var(--curva),
             box-shadow var(--rapido) var(--curva)}
.cupo:hover{transform:translateY(-2px);box-shadow:5px 5px 0 var(--tinta)}
@media(hover:none){.cupo:hover{transform:none;box-shadow:none}}
.cupo i{width:8px;height:8px;background:var(--verde);flex:0 0 auto;
  box-shadow:0 0 0 3px rgba(0,125,85,.18)}
/* El punto respira: dice «hay hueco ahora», y un punto quieto no lo dice. */
@media(prefers-reduced-motion:no-preference){
  .cupo i{animation:latir 2.8s var(--curva) infinite}
  @keyframes latir{0%,100%{box-shadow:0 0 0 3px rgba(0,125,85,.18)}
                   50%{box-shadow:0 0 0 6px rgba(0,125,85,.10)}}}
.acciones{animation:aparecer 560ms var(--entrada) 460ms both}

/* La lámina de la portada. El titular ocupa la izquierda y la derecha se
   quedaba en blanco: esto es lo que la llena, y es el mismo objeto que
   reaparece en cada franja azul. Se retira en cuanto le quitaría sitio al
   texto, no antes. */
.lamina{display:none}
@media(min-width:1120px){
  .portada{position:relative}
  .portada > *{position:relative;z-index:1}
  .lamina{display:block;position:absolute;z-index:0;pointer-events:none;
    right:8px;top:74px;width:284px;height:496px;
    animation:aparecer 640ms var(--entrada) 220ms both}
  .lamina .placa{position:absolute;inset:0;transform:rotate(5deg);
    box-shadow:22px 22px 0 var(--tinta)}
  /* Si la lámina es una imagen, llena el mismo marco: se recorta, no se
     deforma, y conserva la inclinación y la sombra sin desenfoque. */
  .lamina img.placa{width:100%;height:100%;object-fit:cover;display:block}

  /* Aquí iba un barrido de luz sobre el cromo. Retirado: la capa que lo
     recortaba tapaba la lámina entera en lugar de cruzarla. El movimiento de
     esta zona ya lo dan los destellos y el parallax del nombre a sangre; si
     se reintenta, que sea sin una capa a pantalla completa por encima. */
  .lamina .plano{position:absolute;left:-58px;top:96px;width:196px;height:352px;
    background:var(--cobalto);transform:rotate(-6deg)}
  .lamina .chispa{--chispa:96px;left:56%;top:23%}
  .lamina .chispa.baja{--chispa:52px;left:22%;top:71%}}
@media(prefers-reduced-motion:no-preference){
  .lamina .chispa{animation:brillar 4.4s var(--curva) 1s infinite}
  .lamina .chispa.baja{animation-delay:2.6s}}

/* Las cantidades son la interfaz: la tarifa es el objeto más grande de su
   región y los dígitos guardan su sitio. */
.tarifas{display:grid;grid-template-columns:repeat(4,1fr);
  border:1px solid var(--tinta);margin-top:72px}
.tarifas > a{padding:24px 20px 26px;border-right:1px solid var(--tinta);
  text-decoration:none;color:inherit;display:block;position:relative;
  transition:background var(--rapido) var(--curva),
             transform var(--rapido) var(--curva),
             box-shadow var(--rapido) var(--curva)}
.tarifas > a:last-child{border-right:0}
.tarifas > a:hover{background:var(--blanco);transform:translateY(-3px);
  box-shadow:7px 7px 0 var(--tinta);z-index:1}
.tarifas > a:active{transform:translateY(-1px);box-shadow:3px 3px 0 var(--tinta)}
/* El rótulo de la flecha avanza con la tarjeta, que es lo que se ha pulsado. */
.tarifas > a .ir{transition:transform var(--rapido) var(--curva)}
.tarifas > a:hover .ir{transform:translateX(5px)}
.tarifas .que{font-size:15px;color:var(--tinta-2);margin-top:12px;font-weight:300;
  max-width:none}
.tarifas .ir{font-family:var(--display);font-size:14px;font-weight:500;
  letter-spacing:.05em;text-transform:uppercase;color:var(--fuego-texto);
  margin-top:14px;display:block}
@media(hover:none){.tarifas > a:hover{background:transparent;transform:none;
  box-shadow:none}.tarifas > a:hover .ir{transform:none}}
@media(max-width:900px){.tarifas{grid-template-columns:1fr 1fr}
  .tarifas > a:nth-child(2){border-right:0}
  .tarifas > a:nth-child(-n+2){border-bottom:1px solid var(--tinta)}}
@media(max-width:540px){.tarifas{grid-template-columns:1fr}
  .tarifas > a{border-right:0;border-bottom:1px solid var(--tinta)}
  .tarifas > a:last-child{border-bottom:0}}


.prueba{display:grid;gap:38px;align-items:center;margin-top:20px}
@media(min-width:900px){.prueba{grid-template-columns:288px minmax(0,1fr);gap:72px}}
.grandota{font-family:var(--display);font-size:clamp(56px,9vw,124px);line-height:.86;
  letter-spacing:-.02em}
.cero{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:12px;
  font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  border:1px solid var(--fuego-texto);color:var(--fuego-texto);padding:7px 13px}
/* La factura de agosto, con sus cifras de verdad. Antes aquí había barras
   grises simulando un papel: enseñaba la forma de una factura y ninguna de las
   cuentas, que es justo lo único que había que demostrar. Los datos fiscales
   —quién factura, a quién, matrícula e IBAN— van tapados en negro, y se ve que
   están tapados a propósito. */
.factura{width:100%;max-width:340px;justify-self:start;
  border:1px solid var(--tinta);background:var(--blanco);
  padding:22px 22px 24px;display:grid;align-content:start;
  box-shadow:14px 14px 0 var(--tinta);font-family:var(--mono);font-size:11.5px;
  color:var(--tinta-2);line-height:1.5}
.factura .cab{display:flex;justify-content:space-between;align-items:flex-start;
  gap:12px;border-bottom:1px solid var(--tinta);padding-bottom:12px}
.factura .rot{font-family:var(--display);font-size:17px;letter-spacing:.02em;
  text-transform:uppercase;color:var(--tinta);line-height:1}
.factura .serie-f{text-align:right;font-size:10.5px;color:var(--tinta-3);
  white-space:nowrap}
.factura .tapado{display:inline-block;height:9px;background:var(--tinta);
  vertical-align:middle;opacity:.86}
.factura .de{padding:11px 0;border-bottom:1px dashed var(--hilo);
  display:grid;gap:6px}
.factura .et{font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--tinta-3)}
.factura .lin{display:grid;grid-template-columns:1fr auto;gap:10px;
  padding:7px 0;border-bottom:1px solid var(--hilo)}
.factura .lin .u{font-size:10px;color:var(--tinta-3);display:block}
.factura .lin .im{color:var(--tinta);white-space:nowrap;align-self:center}
.factura .sum{display:grid;grid-template-columns:1fr auto;gap:10px;
  padding:5px 0;font-size:11px}
.factura .sum:first-of-type{padding-top:11px}
.factura .sum .im{color:var(--tinta);white-space:nowrap}
.factura .sum.resta .im{color:var(--fuego-texto)}
.factura .tot{display:grid;grid-template-columns:1fr auto;gap:10px;
  align-items:baseline;margin-top:11px;padding-top:12px;
  border-top:1px solid var(--tinta)}
.factura .tot .et{align-self:center}
.factura .tot .im{font-family:var(--display);font-size:26px;color:var(--tinta);
  line-height:1;letter-spacing:.01em}
@media(max-width:900px){.factura{max-width:100%;font-size:12px}}

/* Entra línea a línea, como se lee una factura: de arriba abajo. El escalonado
   arranca cuando el bloque entra en pantalla, no al cargar, y para a los 60 ms
   por línea para que la última no llegue tardísimo. */
@media(prefers-reduced-motion:no-preference){
  .factura .lin,.factura .sum,.factura .tot,.factura .de{opacity:0;
    transform:translateY(9px)}
  .factura.dentro .lin,.factura.dentro .sum,.factura.dentro .tot,
  .factura.dentro .de{animation:lin var(--normal) var(--entrada) both}
  .factura.dentro .de{animation-delay:40ms}
  .factura.dentro .lin:nth-of-type(1){animation-delay:120ms}
  .factura.dentro .lin:nth-of-type(2){animation-delay:180ms}
  .factura.dentro .lin:nth-of-type(3){animation-delay:240ms}
  .factura.dentro .sum:nth-of-type(1){animation-delay:300ms}
  .factura.dentro .sum:nth-of-type(2){animation-delay:340ms}
  .factura.dentro .sum:nth-of-type(3){animation-delay:380ms}
  .factura.dentro .tot{animation-delay:440ms}
  @keyframes lin{to{opacity:1;transform:none}}}

.obras{border-top:1px solid var(--tinta);margin-top:8px}
.obra{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:baseline;
  padding:28px 0;border-bottom:1px solid var(--tinta);text-decoration:none;
  color:inherit;transition:transform var(--normal) var(--expo)}
.obra:hover{transform:translateX(14px)}
@media(hover:none){.obra:hover{transform:none}}
.obra h3{margin-bottom:9px}
.obra .que{font-size:15px;color:var(--tinta-2);font-weight:300;max-width:38rem}
.obra .ir{font-family:var(--mono);font-size:11px;font-weight:600;
  letter-spacing:.16em;text-transform:uppercase;color:var(--fuego-texto);
  white-space:nowrap}
@media(max-width:640px){.obra{grid-template-columns:1fr}.obra .ir{margin-top:12px}}
"""

pagina("index.html",
  t("James J Projects — websites and Google profiles for local businesses",
    "James J Projects — webs y fichas de Google para negocios de barrio"),
  t("Hand-built websites, Google Business Profiles and a menu that lives on the table. Closed prices, said up front.",
    "Webs hechas a mano, fichas de Google y una carta que vive en la mesa. Precios cerrados y dichos de antemano."),
f"""
<main id="principal">
<div class="env">
  <header class="portada">
    <span class="reticula" aria-hidden="true"></span>
    <span class="lamina" aria-hidden="true">
      <span class="plano"></span>
      {f'<img class="placa" src="{A}img/{LAMINA}" alt="" width="284" height="496" fetchpriority="high" decoding="async">'
       if LAMINA else '<span class="placa cromo"></span>'}
      <span class="chispa"></span>
      <span class="chispa baja"></span>
    </span>
    <h1 class="titular">
      <span class="linea"><i>{t("Found","Que te")}</i></span>
      <span class="linea"><i><span class="apagado">{t("on Google.","encuentren en Google")}</span></i></span>
      <span class="linea"><i><em class="subrayado">{t("Walked into.","y entren por la puerta")}</em></i></span>
    </h1>
    <div class="firma">
      <span class="spec">James J Benavides</span>
      <p class="guia">{t(
        "I build the website and put the Google profile in order for bars, garages and corner shops — the ones somebody finds on a phone at nine at night, deciding where to go. I work remotely, so where you are changes nothing.",
        "Hago la web y pongo en orden la ficha de Google de bares, talleres y tiendas de barrio: los negocios que alguien busca en el móvil a las nueve de la noche, decidiendo dónde ir. Trabajo en remoto, así que da igual dónde estés.")}</p>
    </div>
    <div class="cupo"><i></i>{t("Two jobs at a time","Cojo dos encargos a la vez")}</div>
    <div class="acciones">
      <a class="boton boton--lleno" href="mailto:{CORREO}">{t("Ask for a quote","Pedir presupuesto")}</a>
      <a class="boton" href="precios.html">{t("See the prices","Ver los precios")}</a>
    </div>

    <div class="tarifas">
      <a href="ficha-google.html">
        <div class="precio">{v("150–300 €")}<small>{t("one-off","una vez")}</small></div>
        <h2 class="titulo-menor">{t("Google profile","Ficha de Google")}</h2>
        <p class="que">{t("The first thing anyone sees when they look you up. Usually still shows last summer's hours.",
          "Lo primero que ve quien te busca. Suele tener el horario del verano pasado.")}</p>
        <span class="ir">{t("What it covers →","Qué incluye →")}</span></a>
      <a href="precios.html">
        <div class="precio">{v("400–900 €")}<small>{t("closed price","precio cerrado")}</small></div>
        <h2 class="titulo-menor">{t("Full website","Web completa")}</h2>
        <p class="que">{t("One page done properly, not six done badly. Written, not filled in.",
          "Una página bien hecha, no seis mal hechas. Escrita, no rellenada.")}</p>
        <span class="ir">{t("What it covers →","Qué incluye →")}</span></a>
      <a href="carta-nfc.html">
        <div class="precio">{v("120 €")}<small>{t("up to 20 tables","hasta 20 mesas")}</small></div>
        <h2 class="titulo-menor">{t("Menu on the table","Carta en la mesa")}</h2>
        <p class="que">{t("A sticker per table. Tap the phone, the menu opens. Change a price and it changes everywhere.",
          "Una pegatina por mesa. Acercas el móvil y sale la carta. Cambias un precio y cambia en todas.")}</p>
        <span class="ir">{t("See it live →","Verlo funcionando →")}</span></a>
      <a href="caso-factura.html">
        <div class="precio">{v("250 €")}<small>{t("+ 20 € a month","+ 20 € al mes")}</small></div>
        <h2 class="titulo-menor">{t("Photo to invoice","De la foto a la factura")}</h2>
        <p class="que">{t("Send a photo of the day sheet, get the invoice as a PDF with VAT and withholding done.",
          "Mandas la foto de la libreta y sale la factura en PDF, con IVA e IRPF hechos.")}</p>
        <span class="ir">{t("Read the case →","Leer el caso →")}</span></a>
    </div>
  </header>
</div>

<div class="sello" data-lento="0.07" aria-hidden="true"><span>James J Projects<i>®</i></span></div>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("A website is not<br>a printed leaflet","Una web no es<br>un folleto")}</h2>
    <p class="guia sube grande" style="margin-top:28px">{t(
      "A leaflet is printed once and starts going stale that same afternoon. A website gets changed on a Tuesday because you put the set menu up to fourteen euros, and by Wednesday it is right everywhere anyone looks. <b>What I hand you can be changed without calling me, and without paying me twice.</b>",
      "Un folleto se imprime una vez y empieza a quedarse viejo esa misma tarde. Una web se cambia un martes porque has subido el menú a catorce euros, y el miércoles ya está bien en todas partes donde alguien mire. <b>Lo que te entrego se puede cambiar sin llamarme y sin pagarme dos veces.</b>")}</p>
    <div class="hechos sube">
      <div><span class="spec">{t("Owner","Dueño")}</span><div class="dato">{t("You","Tú")}</div></div>
      <div><span class="spec">{t("Template","Plantilla")}</span><div class="dato">{t("None","Ninguna")}</div></div>
      <div><span class="spec">{t("Lock-in","Permanencia")}</span><div class="dato">{t("None","No hay")}</div></div>
      <div><span class="spec">{t("Who builds it","Quién la hace")}</span><div class="dato">{t("Me","Yo")}</div></div>
    </div>
  </div>
</section>

<section class="papel-sec">
  <div class="env">
    <div class="prueba">
      <figure class="factura sube" style="margin:0">
        <div class="cab">
          <span class="rot">{t("Invoice","Factura")}</span>
          <span class="serie-f">Nº 2026/08/001<br>{t("31 August 2026","31 de agosto de 2026")}</span>
        </div>
        <div class="de">
          <div><span class="et">{t("From","De")}</span><br>
            <i class="tapado" style="width:118px"></i></div>
          <div><span class="et">{t("Billed to","Facturar a")}</span><br>
            <i class="tapado" style="width:96px"></i></div>
        </div>
        <div class="lin"><span>{t("Barcelona","Barcelona")}
          <span class="u">{t("14 days","14 días")} · {euros(215)}</span></span>
          <span class="im">{euros(3010)}</span></div>
        <div class="lin"><span>{t("Outside routes","Rutas externas")}
          <span class="u">{t("7 days","7 días")} · {euros(225)}</span></span>
          <span class="im">{euros(1575)}</span></div>
        <div class="lin"><span>{t("Second delivery","2ª entrega")}
          <span class="u">{t("2 extras","2 extras")} · {euros(30)}</span></span>
          <span class="im">{euros(60)}</span></div>
        <div class="sum"><span>{t("Net","Base imponible")}</span>
          <span class="im">{euros(4645)}</span></div>
        <div class="sum"><span>{t("VAT 21%","IVA 21 %")}</span>
          <span class="im">{euros(975,"45")}</span></div>
        <div class="sum resta"><span>{t("Withholding 1%","Retención IRPF 1 %")}</span>
          <span class="im">−{euros(46,"45")}</span></div>
        <div class="tot"><span class="et">{t("Total","Total")}</span>
          <span class="im">{euros(5574)}</span></div>
      </figure>
      <div class="sube">
        <div class="grandota">{euros(5574)}</div>
        <span class="spec" style="margin-top:16px">{t(
          "August 2026 · a real invoice","Agosto de 2026 · una factura real")}</span>
        <div class="cero">{t(f"{euros(0)} difference", f"{euros(0)} de diferencia")}</div>
        <p class="guia" style="margin-top:22px">{t(
          "Twenty-one days written by hand in a notebook. The invoice the system produced came out identical, to the cent, to the one issued by hand. <b>This is the only real proof on this site; everything else is an honest demo and says so.</b>",
          "Veintiuna jornadas apuntadas a mano en una libreta. La factura que sacó el sistema salió idéntica, al céntimo, a la que se emitió a mano. <b>Es la única prueba real de este sitio; lo demás son demos honestas y lo dicen.</b>")}</p>
        <div class="acciones">
          <a class="boton" href="caso-factura.html">{t("Read the whole case","Leer el caso entero")}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="papel-sec" id="trabajos">
  <div class="env">
    <h2 class="sube">{t("Every business<br>its own face","Cada negocio<br>su propia cara")}</h2>
    <p class="guia sube" style="margin:24px 0 40px">{t(
      "This site has my face. The ones below have theirs, because a hairdresser and a garage should not look alike, and neither should look like me. <b>None uses a template.</b>",
      "Esta web tiene mi cara. Las de abajo tienen la suya, porque una peluquería y un taller no deberían parecerse, y ninguno debería parecerse a mí. <b>Ninguna usa plantilla.</b>")}</p>
    <div class="obras">
      <a class="obra sube" href="{DEMO}?mesa=7" target="_blank" rel="noopener">
        <div><h3>{t("A bar, live","Un bar, en vivo")}</h3>
          <p class="que">{t("A working site with its own admin panel. Open it: the top bar says which table you came from, because the sticker carries the number.",
            "Un sitio real con su panel. Ábrelo: la barra de arriba dice desde qué mesa entras, porque la pegatina lleva el número.")}</p></div>
        <span class="ir">{t("Open it →","Abrirlo →")}</span></a>
      <a class="obra sube" href="ficha-google.html">
        <div><h3>{t("A Google profile, before and after","Una ficha de Google, antes y después")}</h3>
          <p class="que">{t("What someone sees on a Saturday at nine at night. Drag the bar and compare.",
            "Lo que ve alguien un sábado a las nueve de la noche. Mueve la barra y compara.")}</p></div>
        <span class="ir">{t("Compare →","Comparar →")}</span></a>
      <a class="obra sube" href="panel-demo.html">
        <div><h3>{t("A dashboard","Un panel")}</h3>
          <p class="que">{t("How many people looked you up and how many called. The figures are invented and the page says so.",
            "Cuánta gente te ha buscado y cuántos han llamado. Las cifras son inventadas y la página lo dice.")}</p></div>
        <span class="ir">{t("See it →","Verlo →")}</span></a>
    </div>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("Tell me about<br>the business","Cuéntame<br>el negocio")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "Twenty minutes on the phone and you get a written quote. <b>The first conversation and the quote cost nothing</b>, and if after the second round of changes you are not convinced, I give back the first half and we owe each other nothing.",
      "Veinte minutos por teléfono y sales con el presupuesto por escrito. <b>La primera conversación y el presupuesto no se cobran</b>, y si a la segunda ronda de cambios no te convence, te devuelvo la primera mitad y no nos debemos nada.")}</p>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="mailto:{CORREO}">{CORREO}</a>
    </div>
  </div>
</section>
</main>
""", CSS_HOME)

# ═══════════════════════════ 2. PRECIOS ═══════════════════════════════
CSS_PRECIOS = """
/* En rejilla, las celdas se estiran a la altura de la fila y la tarjeta con
   menos puntos se quedaba con un palmo de blanco muerto debajo de su lista.
   En columna flexible, el pie se empuja al fondo con `margin-top:auto` y las
   dos tarjetas de una fila terminan a la misma altura, con la misma línea. */
.tarjeta{border:1px solid var(--tinta);padding:28px;display:flex;
  flex-direction:column;gap:0}
.pie-t{margin-top:auto;padding-top:20px;display:flex;flex-wrap:wrap;
  align-items:baseline;justify-content:space-between;gap:12px}
.pie-t .ir-t{font-family:var(--display);font-size:14px;font-weight:500;
  letter-spacing:.05em;text-transform:uppercase;color:var(--fuego-texto);
  text-decoration:none;white-space:nowrap;
  transition:transform var(--rapido) var(--curva)}
.pie-t .ir-t:hover{transform:translateX(5px)}
@media(hover:none){.pie-t .ir-t:hover{transform:none}}
.rejilla{display:grid;gap:0;border:1px solid var(--tinta);margin-top:14px}
.rejilla > .tarjeta{border:0;border-bottom:1px solid var(--tinta)}
.rejilla > .tarjeta:last-child{border-bottom:0}
@media(min-width:820px){
  .rejilla{grid-template-columns:1fr 1fr}
  .rejilla > .tarjeta{border-bottom:1px solid var(--tinta);
    border-right:1px solid var(--tinta)}
  .rejilla > .tarjeta:nth-child(2n){border-right:0}
  .rejilla > .tarjeta:nth-last-child(-n+2){border-bottom:0}}
.tarjeta h2{margin:16px 0 10px}
.tarjeta .que{color:var(--tinta-2);font-weight:300;font-size:15.5px}
.lista{list-style:none;padding:18px 0 0;margin:18px 0 0;
  border-top:1px solid var(--hilo);display:grid;gap:9px}
.lista li{font-size:14.5px;color:var(--tinta-2);padding-left:17px;position:relative}
.lista li::before{content:"";position:absolute;left:0;top:9px;width:6px;height:6px;
  background:var(--fuego)}
.aviso-t{font-size:13.5px;color:var(--tinta-3);line-height:1.6;
  flex:1 1 15rem;min-width:0;margin:0}
.pie-t{border-top:1px solid var(--hilo);margin-top:auto}
.faq{border-top:1px solid var(--tinta);margin-top:56px}
.faq > div{padding:26px 0;border-bottom:1px solid var(--hilo)}
.faq h3{margin-bottom:10px}
.faq p{color:var(--tinta-2);font-weight:300;font-size:16px}
"""

def tarjeta(precio, unidad, titulo, que, puntos, nota="", destacada=False):
    lis = "".join(f"<li>{x}</li>" for x in puntos)
    aviso = f'<p class="aviso-t">{nota}</p>' if nota else '<span></span>'
    return f"""<div class="tarjeta{' destacada' if destacada else ''}">
    <div class="precio">{precio}<small>{unidad}</small></div>
    <h2 class="titulo-menor">{titulo}</h2><p class="que">{que}</p>
    <ul class="lista">{lis}</ul>
    <div class="pie-t">{aviso}
      <a class="ir-t" href="mailto:{CORREO}">{t("Ask for this →","Pedirlo →")}</a>
    </div></div>"""

pagina("precios.html",
  t("Pricing — James J Projects","Precios — James J Projects"),
  t("Closed prices, written down. What each service costs and what it covers.",
    "Precios cerrados y por escrito. Qué cuesta cada servicio y qué incluye."),
f"""
<main id="principal">
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("What it costs,<br>and why","Lo que cuesta,<br>y por qué")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "Asking a price and being told <b>“it depends”</b> is the part everyone dreads. Here it is written down. The quote closes before the work starts: what is said is what is paid, with nothing added at the end.",
      "Preguntar el precio y que te digan <b>«depende»</b> es la parte que a todo el mundo le da pereza. Aquí está escrito. El presupuesto se cierra antes de empezar: lo que se dice es lo que se paga, sin extras al final.")}</p>

    <div class="rejilla sube">
      {tarjeta(v("150–300 €"), t("one-off","una vez"), t("Google profile in order","Ficha de Google en condiciones"),
        t("The first thing a customer sees when they look you up. It is usually stuck on hours from two summers ago, with no decent photo.",
          "Lo primero que ve un cliente cuando busca tu negocio. Suele estar con el horario de hace dos veranos y sin una foto decente."),
        [t("Photos, hours and services up to date","Fotos, horarios y servicios al día"),
         t("Written replies to the reviews you owe","Respuesta escrita a las reseñas pendientes"),
         t("I teach you to answer them yourself in ten minutes","Te enseño a contestarlas tú en diez minutos")])}
      {tarjeta(v("400–900 €"), t("closed price","precio cerrado"), t("Full website","Web completa del negocio"),
        t("One page done properly, not six done badly. What you do, where you are, what it costs and how to reach you.",
          "Una página bien hecha, no seis mal hechas. Qué haces, dónde estás, cuánto cuesta y cómo se te llama."),
        [t("Designed for you, no template","Diseño a medida, sin plantilla"),
         t("Copy written, not filled in","Textos escritos, no rellenados"),
         t("Loads fast on a bad connection","Carga rápido aunque haya poca cobertura"),
         t("Shows up on Google, with a WhatsApp button","Aparecer en Google y botón de WhatsApp"),
         t("Domain and hosting sorted","Dominio y alojamiento resueltos"),
         t("Two rounds of changes included","Dos rondas de cambios incluidas")])}
      {tarjeta(v("120 €"), t("up to 20 tables · +3 € each extra","hasta 20 mesas · +3 € por mesa de más"),
        t("Menu on the table","La carta, pegada en la mesa"),
        t("A sticker on every table. The customer taps their phone and your menu opens, with photos, prices and allergens.",
          "Una pegatina en cada mesa. El cliente acerca el móvil y sale tu carta con fotos, precios y alérgenos."),
        [t("Chip inside <b>and the code printed on top</b>: works on any phone","Chip dentro <b>y el código impreso encima</b>: funciona con cualquier móvil"),
         t("Survives daily cleaning","Aguanta la limpieza diaria"),
         t("Change a price and it changes on every table at once","Cambias un precio y cambia en todas las mesas a la vez"),
         t("Each sticker carries its table number","Cada pegatina lleva su número de mesa"),
         t("Allergens always current, which is a legal requirement","Alérgenos siempre al día, que es obligatorio")],
        t('Photos are yours, taken with your phone. <a href="carta-nfc.html">How it works →</a>',
          'Las fotos son tuyas, hechas con tu móvil. <a href="carta-nfc.html">Cómo funciona →</a>'))}
      {tarjeta(v("250 €"), t("setup, then 20 € a month","montaje, y 20 € al mes"),
        t("Photo to invoice","De la foto a la factura"),
        t("If you charge by the day, the route or the job and month-end means sitting down to add up a notebook, this does it for you.",
          "Si cobras por jornadas, rutas o servicios y a fin de mes te toca sentarte a sumar la libreta, esto lo hace por ti."),
        [t("Reads handwriting and shows you line by line what it understood","Lee la letra a mano y te enseña línea por línea lo que ha entendido"),
         t("Issues nothing until you confirm the money","No emite nada hasta que tú confirmas el dinero"),
         t("Fuel and toll receipts filed as expenses","Los tickets de gasoil y peajes se guardan como gasto"),
         t("Reminder on the 28th so it does not slip","Aviso el día 28 para que no se te pase"),
         t("CSV summary for your accountant","Resumen en CSV para tu gestoría")],
        t('Not an advisory service and it does not tell you what to declare. <a href="caso-factura.html">The real case →</a>',
          'No es una asesoría y no te dice qué declarar. <a href="caso-factura.html">El caso real →</a>'))}
      {tarjeta(v("30–50 €"), t("a month, no lock-in","al mes, sin permanencia"), t("Keeping it current","Que no se quede vieja"),
        t("Changes to the menu, the prices, the hours and the photos whenever they are needed.",
          "Cambios de carta, de precios, de horarios y de fotos cuando hagan falta."),
        [t("Unlimited changes within 48 hours","Cambios ilimitados en 48 horas"),
         t("Backup and monitoring","Copia de seguridad y vigilancia"),
         t("One note a month on how the site is doing","Un aviso al mes con cómo va la web")])}
      {tarjeta(v("0 €"), t("always included","siempre incluido"), t("What I do not charge for","Lo que no te cobro"),
        t("Before you commit to anything.","Antes de que te comprometas a nada."),
        [t("The first conversation","La primera conversación"),
         t("Telling you what your profile is missing","Decirte qué le falta a tu ficha"),
         t("The written quote","El presupuesto por escrito")])}
    </div>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("Half up front,<br>half when you like it","La mitad al empezar,<br>la mitad cuando te gusta")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "You see the site finished and working before you pay the rest, not a mock-up. If after the second round of changes it does not convince you, I return the first half and we owe each other nothing. Transfer, Bizum or a proper invoice with VAT.",
      "Ves la web terminada y funcionando antes de pagar el resto, no un boceto. Si a la segunda ronda de cambios no te convence, te devuelvo la primera mitad y no nos debemos nada. Transferencia, Bizum o factura con IVA.")}</p>
  </div>
</section>

<section class="papel-sec">
  <div class="env">
    <h2 class="sube">{t("What people ask","Lo que suelen preguntar")}</h2>
    <div class="faq sube">
      <div><h3>{t("Why so cheap compared to an agency?","¿Por qué tan barato comparado con una agencia?")}</h3>
        <p>{t("Because there is no agency. You are not paying for salespeople, an office, or the person who passes your work to someone else. I work alone and in the afternoons, and that is also my limit: I cannot take ten sites at once.",
          "Porque no hay agencia. No pagas comerciales, ni oficina, ni al que le pasa el trabajo a otro. Trabajo solo y por las tardes, y por eso también tengo un límite: no puedo coger diez webs a la vez.")}</p></div>
      <div><h3>{t("Is the site actually mine?","¿La web es mía de verdad?")}</h3>
        <p>{t("Yes. The domain is registered in your name and the keys stay with you. If tomorrow you want to go elsewhere, you take everything. I do not hold websites hostage, which is the practice that makes so many people distrust this trade.",
          "Sí. El dominio se pone a tu nombre y las claves quedan en tu mano. Si mañana quieres irte con otro, te vas con todo. No secuestro webs, que es la práctica que hace que tanta gente desconfíe.")}</p></div>
      <div><h3>{t("How long does it take?","¿Cuánto tarda?")}</h3>
        <p>{t("A week from the moment you send me the photos and the text. The Google profile, the same day. What usually delays a job is not me: it is the material taking time to arrive.",
          "Una semana desde que me pasas las fotos y los textos. La ficha de Google, el mismo día. Lo que suele retrasar un encargo no soy yo: es que el material tarda en llegar.")}</p></div>
      <div><h3>{t("I have no good photos of the place.","No tengo fotos buenas del local.")}</h3>
        <p>{t("I go and take them. It is included in the website and in the profile. With a current phone and good light it comes out better than most stock photography — and better than anything generated by a computer, which Google rejects on business profiles.",
          "Voy y las hago. Va incluido en la web y en la ficha. Con un móvil actual y buena luz sale mejor que la mayoría de las fotos de banco, y mejor que cualquier cosa generada por ordenador, que Google rechaza en las fichas de negocio.")}</p></div>
      <div><h3>{t("Does the table sticker work for my trade?","¿Lo de la pegatina vale para mi oficio?")}</h3>
        <p>{t("It works anywhere a customer sits down: bars, restaurants, terraces, waiting rooms. What it does not cover is a shop with no seating — there the profile and the website do more.",
          "Vale donde el cliente se sienta: bares, restaurantes, terrazas, salas de espera. Lo que no cubre es una tienda sin mesas: ahí hacen más la ficha y la web.")}</p></div>
    </div>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="mailto:{CORREO}">{t("Ask for a quote","Pedir presupuesto")}</a>
      <a class="boton" href="caso-factura.html">{t("See real work","Ver un trabajo hecho")}</a>
    </div>
  </div>
</section>
</main>
""", CSS_PRECIOS)

# ═══════════════════ 3. LA CARTA EN LA MESA ═══════════════════════════
CSS_NFC = """
.escena{position:relative;height:340px;display:grid;place-items:end center;
  padding-bottom:28px;overflow:hidden;background:var(--cobalto);
  margin-inline:calc(50% - 50vw);margin-top:44px}
.tablero{position:absolute;left:0;right:0;bottom:0;height:38%;
  background:linear-gradient(180deg,#c8ab86,#a8875f)}
.tablero::before{content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(90deg,rgba(0,0,0,.06) 0 2px,transparent 2px 26px)}
.pegatina{position:absolute;left:62%;bottom:12%;transform:translateX(-50%);
  width:66px;height:66px;background:var(--blanco);z-index:1;display:grid;
  place-items:center;font-family:var(--mono);font-size:8px;font-weight:600;
  letter-spacing:.1em;color:var(--tinta-2);text-align:center;line-height:1.4;
  box-shadow:8px 8px 0 rgba(0,0,0,.3)}
.pegatina b{display:block;font-size:14px;letter-spacing:0;color:var(--tinta)}
.onda{position:absolute;left:62%;bottom:12%;width:66px;height:66px;
  transform:translateX(-50%);border:2px solid var(--fuego);opacity:0}
.movil{position:relative;z-index:2;width:122px;height:226px;background:var(--tinta);
  padding:7px;box-shadow:14px 14px 0 rgba(0,0,0,.42)}
.movil .pantalla{width:100%;height:100%;background:var(--blanco);overflow:hidden;
  position:relative}
.cartita{position:absolute;inset:0;padding:9px;opacity:0}
.cartita .cab{height:32px;background:var(--fuego-fondo);margin-bottom:8px;display:grid;
  place-items:center;color:#fff;font-family:var(--mono);font-size:7px;
  letter-spacing:.14em}
.cartita .ln{height:7px;background:var(--hueco);margin-bottom:5px}
.cartita .ln.corta{width:56%}
.cartita .ln.eur{width:32%;background:var(--fuego);opacity:.5}
@media(prefers-reduced-motion:no-preference){
  .movil{animation:acercar 4.4s var(--curva) infinite}
  .onda{animation:onda 4.4s var(--curva) infinite}
  .onda.dos{animation-delay:.24s}
  .cartita{animation:mostrar 4.4s var(--curva) infinite}
  @keyframes acercar{0%{transform:translate(-46px,-84px) rotate(-9deg)}
    30%,78%{transform:translate(-64px,-16px) rotate(-3deg)}
    100%{transform:translate(-46px,-84px) rotate(-9deg)}}
  @keyframes onda{0%,32%{transform:translateX(-50%) scale(1);opacity:0}
    40%{opacity:.85}56%,100%{transform:translateX(-50%) scale(2.4);opacity:0}}
  @keyframes mostrar{0%,40%{opacity:0;transform:translateY(8px)}
    50%,74%{opacity:1;transform:none}84%,100%{opacity:0}}}
@media(prefers-reduced-motion:reduce){
  .movil{transform:translate(-64px,-16px) rotate(-3deg)}.cartita{opacity:1}}

"""

pagina("carta-nfc.html",
  t("The menu, stuck to the table — James J Projects","La carta, pegada en la mesa — James J Projects"),
  t("A sticker on every table opens your live menu. Change a price once and it changes on every table.",
    "Una pegatina en cada mesa abre tu carta. Cambias un precio una vez y cambia en todas."),
f"""
<main id="principal">
<section class="papel-sec" style="padding-top:132px;padding-bottom:0">
  <div class="env">
    <h1>{t("The menu,<br>stuck to the table","La carta,<br>pegada en la mesa")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "<b>A sticker on every table. The customer taps their phone and your menu opens.</b> No camera, no focusing, nothing to download. And when you raise a price you change it yourself from your phone: nothing needs reprinting, because nothing is printed.",
      "<b>Una pegatina en cada mesa. El cliente acerca el móvil y sale tu carta.</b> Sin cámara, sin enfocar, sin descargar nada. Y cuando subes un precio lo cambias tú desde el móvil: no hay que reimprimir nada, porque no hay nada impreso.")}</p>
  </div>
  <div class="escena" aria-hidden="true">
    <div class="tablero"></div>
    <div class="onda"></div><div class="onda dos"></div>
    <div class="pegatina"><span>NFC<b>+QR</b></span></div>
    <div class="movil"><div class="pantalla"><div class="cartita">
      <div class="cab">{t("TABLE 7","MESA 7")}</div>
      <div class="ln"></div><div class="ln corta"></div><div class="ln eur"></div>
      <div class="ln" style="margin-top:9px"></div><div class="ln corta"></div><div class="ln eur"></div>
      <div class="ln" style="margin-top:9px"></div><div class="ln corta"></div><div class="ln eur"></div>
    </div></div></div>
  </div>
  <div class="env">
    <p class="guia" style="margin-top:22px;font-size:16px">{t(
      "The sticker carries the chip inside <b>and the code printed on top</b>: if a phone has no antenna, or has it switched off, the camera still works. Nobody is left out.",
      "La pegatina lleva el chip dentro <b>y el código impreso encima</b>: si el móvil no tiene antena o la lleva apagada, la cámara sirve igual. Nadie se queda fuera.")}</p>
  </div>
</section>

<section class="papel-sec">
  <div class="env">
    <h2 class="sube">{t("Four steps","Cuatro pasos")}</h2>
    <div class="pasos sube" style="margin-top:32px">
      <div class="paso"><span class="n">01</span><div>
        <h3>{t("Send me the menu however you have it","Me pasas la carta como la tengas")}</h3>
        <p>{t("A sheet of paper, a photo, an old PDF. I put it into the system with its prices, its allergens and its sections.",
          "Un papel, una foto, un PDF viejo. Yo la paso al sistema con sus precios, sus alérgenos y sus categorías.")}</p></div></div>
      <div class="paso"><span class="n">02</span><div>
        <h3>{t("You take the photos with your phone","Haces las fotos con tu móvil")}</h3>
        <p>{t("In daylight, no filters. Nothing generated by a computer: Google rejects generated photos on business profiles, and since 2 August 2026 European law requires labelling them. A real photo avoids both, and it is what is actually on the plate.",
          "Con luz de día y sin filtros. Nada generado por ordenador: Google rechaza las fotos generadas en la ficha, y desde el 2 de agosto de 2026 el reglamento europeo obliga a etiquetarlas. Una foto real evita las dos cosas y además es lo que hay en el plato.")}</p></div></div>
      <div class="paso"><span class="n">03</span><div>
        <h3>{t("I stick one on every table","Pego una pegatina en cada mesa")}</h3>
        <p>{t("Each one carries its number inside. When someone opens it from table 7, the WhatsApp button arrives already written: “I'm at table 7”. A photocopied code cannot do that.",
          "Cada una lleva su número dentro. Cuando alguien la usa desde la mesa 7, el botón de WhatsApp le sale ya escrito con «estoy en la mesa 7». Un código fotocopiado no puede hacer eso.")}</p></div></div>
      <div class="paso"><span class="n">04</span><div>
        <h3>{t("From then on, you run it","A partir de ahí, la manejas tú")}</h3>
        <p>{t("You log in from your phone, change a price, and it changes on every table at once. Seasonal menus without throwing the old ones in the bin.",
          "Entras desde el móvil, cambias un precio y cambia en todas las mesas a la vez. Cartas de temporada sin tirar las viejas a la basura.")}</p></div></div>
    </div>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="{DEMO}?mesa=7" target="_blank" rel="noopener">{t("Open a real menu","Abrir una carta de verdad")}</a>
      <a class="boton" href="precios.html">{t("What it costs","Cuánto cuesta")}</a>
    </div>
    <p class="spec sube" style="margin-top:16px;letter-spacing:.14em;line-height:1.9">{t(
      "That link is a real table. Look at the bar at the top and the button at the bottom.",
      "Ese enlace es el de una mesa real: fíjate en la barra de arriba y en el botón de abajo.")}</p>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("One menu,<br>two doors","Una carta,<br>dos puertas")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "What opens when the phone touches the table <b>is your website</b>. The same one that shows up on Google when somebody looks you up from home, and the same one you link from your social accounts. These are not two products: it is one, with a door in the customer's pocket and a door on the table.",
      "Lo que se abre al acercar el móvil <b>es tu web</b>. La misma que sale en Google cuando alguien te busca desde casa, y la misma que enseñas en tus redes. No son dos productos: es uno con dos puertas, una en el bolsillo del cliente y otra en la mesa.")}</p>
    <p class="guia sube" style="margin-top:16px">{t(
      "That is why it costs less together than separately, and why the stickers are so cheap: the hard work is already done once you have the website.",
      "Por eso sale más barato hacerlo junto que por separado, y por eso el precio de las pegatinas es tan bajo: el trabajo gordo ya está hecho cuando tienes la web.")}</p>
  </div>
</section>
</main>
""", CSS_NFC)

# ═══════════════ 4, 5 y 6: FICHA, CASO Y PANEL ════════════════════════
CSS_RESTO = """
.comparar{position:relative;border:1px solid var(--tinta);overflow:hidden;
  display:grid;margin-top:40px;touch-action:pan-y;background:var(--hueco)}
.lado{grid-area:1/1;padding:22px;display:grid;align-items:center;min-width:0}
.comparar{min-width:0}
.ficha-g,.fila-g,.fila-g > div,.fot-g{min-width:0}
.tit-g,.sub-g,.res-g{overflow-wrap:anywhere}
.lado.antes{background:var(--hueco)}
.lado.desp{background:var(--blanco);clip-path:inset(0 0 0 52%)}
.rot-lado{position:absolute;top:12px;font-family:var(--mono);font-size:11px;
  font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  background:var(--tinta);color:var(--papel);padding:4px 9px;z-index:3}
.rot-lado.izq{left:12px}.rot-lado.der{right:12px}
.ficha-g{background:var(--blanco);border:1px solid var(--hilo);padding:18px;
  display:grid;gap:13px;align-content:start}
.antes .ficha-g{border-color:var(--hilo)}
.fila-g{display:flex;align-items:flex-start;justify-content:space-between;
  gap:12px;flex-wrap:wrap}
.tit-g{font-size:18px;font-weight:600;color:#1a0dab;white-space:normal}
.sub-g{font-size:13px;color:var(--tinta-2)}
.chip-g{font-family:var(--mono);font-size:11px;font-weight:600;padding:4px 9px;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.chip-g.cerrado{background:#fbe9e6;color:#a3271a}
.chip-g.abierto{background:#e8f6ef;color:var(--verde)}
.fot-g{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.fot-g img,.fot-g i{display:block;width:100%;max-width:100%;min-width:0;
  aspect-ratio:4/3;object-fit:cover;background:var(--hueco)}
.res-g{font-size:12.5px;color:var(--tinta-2)}
.acc-g{display:flex;gap:6px;flex-wrap:wrap}
.acc-g span{font-family:var(--mono);font-size:11px;font-weight:600;
  border:1px solid var(--azul);color:var(--azul);padding:4px 8px;
  letter-spacing:.06em}
.tirador{position:absolute;top:0;bottom:0;left:52%;width:2px;background:var(--tinta);
  z-index:4;cursor:ew-resize}
.tirador::after{content:"";position:absolute;top:50%;left:50%;width:38px;height:38px;
  transform:translate(-50%,-50%);background:var(--tinta);border-radius:50%}
.tirador span{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  z-index:1;color:var(--papel);display:block}
.tirador svg{width:22px;height:12px;display:block}
.tirador:focus-visible{outline:2px solid var(--fuego-fondo);outline-offset:4px}
@media(max-width:760px){.fot-g{grid-template-columns:repeat(3,1fr)}
  .fot-g > :nth-child(4){display:none}.lado{padding:12px}
  .rot-lado{top:8px}.rot-lado.izq{left:8px}.rot-lado.der{right:8px}}

.numeros{display:grid;grid-template-columns:repeat(3,1fr);
  border:1px solid var(--tinta);margin-top:36px}
.numeros > div{padding:22px 20px;border-right:1px solid var(--tinta)}
.numeros > div:last-child{border-right:0}
.numeros .dato{font-family:var(--display);font-size:clamp(30px,4.4vw,52px);
  line-height:1;margin-top:9px}
@media(max-width:700px){.numeros{grid-template-columns:1fr}
  .numeros > div{border-right:0;border-bottom:1px solid var(--tinta)}
  .numeros > div:last-child{border-bottom:0}}
/* La serie de doce semanas. Barras planas de cobalto, filo duro y una sola
   marcada: la que cuenta la historia. Sin librería y sin imagen. */
.serie{border:1px solid var(--tinta);border-top:0;padding:26px 22px 18px}
.serie .barras{display:grid;grid-template-columns:repeat(12,1fr);gap:7px;
  align-items:end;height:172px}
.serie .barras > i{display:block;background:var(--cobalto);
  transform-origin:bottom;animation:crecer 520ms var(--expo) both}
.serie .barras > i.cima{background:var(--fuego)}
@keyframes crecer{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.serie .eje{display:flex;justify-content:space-between;margin-top:10px;
  border-top:1px solid var(--hilo);padding-top:9px}
.serie figcaption{margin-top:14px}
.oculto{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);
  white-space:nowrap}
@media(max-width:560px){.serie .barras{height:132px;gap:4px}}
@media(prefers-reduced-motion:reduce){.serie .barras > i{animation:none}}
/* Las tres cifras de arriba estaban sueltas: 1.284, 96 y 212 no dicen nada
   hasta que se ven una contra otra. El embudo las pone en escala y enseña lo
   único que un dueño quiere saber: de los que te buscan, cuántos hacen algo. */
.embudo{border:1px solid var(--tinta);border-top:0;padding:24px 22px 20px}
.embudo .paso-e{display:grid;grid-template-columns:1fr;gap:7px;
  padding:13px 0;border-bottom:1px solid var(--hilo)}
.embudo .paso-e:last-of-type{border-bottom:0}
.embudo .fila-e{display:flex;align-items:baseline;justify-content:space-between;
  gap:14px}
.embudo .qui{font-size:15px;color:var(--tinta-2);font-weight:300}
.embudo .cifra{font-family:var(--display);font-size:clamp(22px,3.2vw,32px);
  line-height:1;color:var(--tinta);white-space:nowrap}
.embudo .cifra small{font-family:var(--mono);font-size:11px;font-weight:600;
  letter-spacing:.1em;color:var(--tinta-3);margin-left:9px}
.embudo .via{height:13px;background:var(--hueco);overflow:hidden}
.embudo .via > i{display:block;height:100%;background:var(--cobalto);
  transform-origin:left;transform:scaleX(0)}
.embudo .paso-e:last-of-type .via > i{background:var(--fuego)}
.embudo.dentro .via > i{animation:medir 520ms var(--expo) both}
@keyframes medir{to{transform:scaleX(1)}}
.embudo .paso-e:nth-of-type(2) .via > i{animation-delay:110ms}
.embudo .paso-e:nth-of-type(3) .via > i{animation-delay:220ms}
@media(prefers-reduced-motion:reduce){
  .embudo .via > i{transform:scaleX(1);animation:none}}

.aviso-demo{border:1px solid var(--fuego-texto);padding:18px 20px;margin-top:32px;
  font-size:15px;color:var(--tinta-2);font-weight:300}
.aviso-demo b{color:var(--fuego-texto);font-weight:600}
"""

JS_COMPARAR = """
const c=document.querySelector('.comparar');
if(c){const d=c.querySelector('.lado.desp'),t=c.querySelector('.tirador');
let arrastra=false;
const antes=c.dataset.antes||'before',desp=c.dataset.desp||'after';
const poner=x=>{const r=c.getBoundingClientRect();
  const p=Math.min(96,Math.max(4,((x-r.left)/r.width)*100));
  d.style.clipPath=`inset(0 0 0 ${p}%)`;t.style.left=p+'%';
  const n=Math.round(p);t.setAttribute('aria-valuenow',String(n));
  t.setAttribute('aria-valuetext',n+'% '+antes+', '+(100-n)+'% '+desp);};
/* El tirador arranca en el 52% que pinta el CSS: si no se siembra, la primera
   flecha lo manda al 52 otra vez en vez de moverlo. */
t.style.left='52%';poner(c.getBoundingClientRect().left+.52*c.getBoundingClientRect().width);
const inicio=e=>{arrastra=true;poner((e.touches?e.touches[0]:e).clientX);};
const mover=e=>{if(!arrastra)return;poner((e.touches?e.touches[0]:e).clientX);};
const fin=()=>{arrastra=false;};
c.addEventListener('mousedown',inicio);c.addEventListener('touchstart',inicio,{passive:true});
window.addEventListener('mousemove',mover);window.addEventListener('touchmove',mover,{passive:true});
window.addEventListener('mouseup',fin);window.addEventListener('touchend',fin);
t.addEventListener('keydown',e=>{
  const actual=parseFloat(t.style.left)||52;let p=null;
  if(e.key==='ArrowLeft'||e.key==='ArrowRight') p=actual+(e.key==='ArrowLeft'?-4:4);
  else if(e.key==='Home') p=4; else if(e.key==='End') p=96;
  if(p===null)return;
  e.preventDefault();poner(c.getBoundingClientRect().left+(p/100)*c.getBoundingClientRect().width);});}
"""

def ficha_google(estado, hrs, fotos, resenas, acciones):
    return f"""<div class="ficha-g">
      <div class="fila-g"><div><div class="tit-g">Bar Marina</div>
        <div class="sub-g">{t("Tapas bar · sample profile","Bar de tapas · ficha de ejemplo")}<br>{hrs}</div></div>
        {estado}</div>
      <div class="fot-g">{fotos}</div>
      <div class="fila-g"><span class="res-g">{resenas}</span><div class="acc-g">{acciones}</div></div>
    </div>"""

pagina("ficha-google.html",
  t("Your Google profile — James J Projects","Tu ficha de Google — James J Projects"),
  t("The profile with the map beside it is the first thing a customer judges. Drag the bar and compare.",
    "La ficha que sale con el mapa al lado es lo primero que juzga un cliente. Mueve la barra y compara."),
f"""
<main id="principal">
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("The same profile,<br>before and after","La misma ficha,<br>antes y después")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "<b>Before they reach your website, people see you on Google.</b> That panel with the map beside it is the first thing a customer judges. In eight out of ten neighbourhood businesses it still shows hours from two summers ago and three blurry photos somebody else took.",
      "<b>Antes de entrar en tu web, la gente te ve en Google.</b> Esa ficha, la que sale con el mapa al lado, es lo primero que juzga un cliente. Y en ocho de cada diez negocios de barrio está con el horario de hace dos veranos y tres fotos borrosas hechas por otros.")}</p>
    <p class="spec" style="margin-top:22px;letter-spacing:.16em">{t("Drag the bar","Arrastra la barra")}</p>

    <div class="comparar sube"
      data-antes="{t('before','antes')}" data-desp="{t('after','después')}">
      <span class="rot-lado izq">{t("Before","Antes")}</span>
      <span class="rot-lado der">{t("After","Después")}</span>
      <div class="lado antes">{ficha_google(
        f'<span class="chip-g cerrado">{t("Closed","Cerrado")}</span>',
        t("Says closed · opens at 8:00","Dice cerrado · abre a las 8:00"),
        f'<img src="{A}img/mal-local.jpg" width="360" height="270" loading="lazy" alt="{t(
           "The same photo of the room, dark and out of focus",
           "La misma foto de la sala, oscura y desenfocada")}">'
        f'<img src="{A}img/mal-barra.jpg" width="360" height="270" loading="lazy" alt="{t(
           "The same photo of the beer, washed out and blurred",
           "La misma foto de la caña, lavada y movida")}">'
        f'<i role="img" aria-label="{t("Empty photo slot","Hueco de foto vacío")}"></i>'
        f'<i role="img" aria-label="{t("Empty photo slot","Hueco de foto vacío")}"></i>',
        t("6 reviews with no reply","Sin responder a 6 reseñas"), "")}</div>
      <div class="lado desp">{ficha_google(
        f'<span class="chip-g abierto">{t("Open","Abierto")}</span>',
        t("Open · closes at 23:30","Abierto · cierra a las 23:30"),
        f'<img src="{A}img/bien-local.jpg" width="360" height="270" loading="lazy" alt="{t(
           "The room at night, the counter lit from behind",
           "La sala de noche, con la barra iluminada por detrás")}">'
        f'<img src="{A}img/bien-barra.jpg" width="360" height="270" loading="lazy" alt="{t(
           "A beer on an outdoor table, daylight",
           "Una caña en una mesa de fuera, con luz de día")}">'
        f'<img src="{A}img/bien-plato.jpg" width="360" height="270" loading="lazy" alt="{t(
           "A hand lifting a slice out of the pizza box",
           "Una mano sacando una porción de la caja de pizza")}">'
        f'<img src="{A}img/bien-tapa.jpg" width="360" height="270" loading="lazy" alt="{t(
           "A bowl of chips on the counter",
           "Un bol de patatas fritas sobre la barra")}">',
        t("6 reviews answered","6 reseñas contestadas"),
        f'<span>{t("Call","Llamar")}</span><span>{t("Directions","Cómo llegar")}</span><span>Web</span>')}</div>
      <div class="tirador" role="slider" tabindex="0"
        aria-label="{t('Drag to compare the profile before and after','Arrastra para comparar la ficha antes y después')}"
        aria-valuemin="0" aria-valuemax="100" aria-valuenow="52"
        aria-valuetext="{t('52% before, 48% after','52% antes, 48% después')}"
        ><span aria-hidden="true"><svg viewBox="0 0 22 12" fill="none"
        stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
        stroke-linejoin="round"><path d="M6 2 2 6l4 4M16 2l4 4-4 4"/></svg></span></div>
    </div>
    <p class="guia" style="margin-top:20px;font-size:16px">{t(
      "Example business. What changes is not the design: it is that the hours are true, that you took the photos yourself, and that the reviews have been answered.",
      "Negocio de ejemplo. Lo que cambia no es el diseño: es que el horario sea el de verdad, que las fotos las hayas hecho tú y que las reseñas estén contestadas.")}</p>
    <p class="nota" style="margin-top:14px">{t(
      "About these photos: the four on the right are ordinary photographs. The two on the left are two of those same photographs, darkened and blurred on purpose — a neglected profile does not have different photos, it has these ones taken badly. Nothing here is computer-generated, because Google rejects generated photos on a business profile.",
      "Sobre estas fotos: las cuatro de la derecha son fotografías normales. Las dos de la izquierda son dos de esas mismas fotografías, oscurecidas y desenfocadas a propósito — una ficha abandonada no tiene otras fotos, tiene estas mal hechas. Aquí no hay nada generado por ordenador, porque Google rechaza las fotos generadas en una ficha de negocio.")}</p>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <div class="env">
    <h2 class="sube">{t("What I actually do","Lo que hago de verdad")}</h2>
    <div class="hechos sube">
      <div><span class="spec">{t("Hours","Horarios")}</span><div class="dato">{t("True ones","Los de verdad")}</div></div>
      <div><span class="spec">{t("Photos","Fotos")}</span><div class="dato">{t("Yours","Tuyas")}</div></div>
      <div><span class="spec">{t("Reviews","Reseñas")}</span><div class="dato">{t("Answered","Contestadas")}</div></div>
      <div><span class="spec">{t("Takes","Tarda")}</span><div class="dato">{t("One day","Un día")}</div></div>
    </div>
    <p class="guia sube" style="margin-top:34px">{t(
      "And I show you how to answer the next ones yourself in ten minutes, because a review answered three weeks late is worth less than one answered the same evening.",
      "Y te enseño a contestar las siguientes tú en diez minutos, porque una reseña contestada tres semanas tarde vale menos que una contestada esa misma noche.")}</p>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="precios.html">{v("150–300 €")}</a>
      <a class="boton" href="mailto:{CORREO}">{t("Talk to me","Hablamos")}</a>
    </div>
  </div>
</section>
</main>
""", CSS_RESTO, JS_COMPARAR)

pagina("caso-factura.html",
  t("A real case: 5,574.00 € to the cent — James J Projects",
    "Un caso real: 5.574,00 € al céntimo — James J Projects"),
  t("Twenty-one handwritten days turned into an invoice that matched the hand-issued one exactly.",
    "Veintiuna jornadas escritas a mano convertidas en una factura idéntica a la emitida a mano."),
f"""
<main id="principal">
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("Twenty-one days<br>in a notebook","Veintiuna jornadas<br>en una libreta")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "A self-employed driver invoices one company every month. Twenty-one working days written by hand: a date, a route, sometimes a second delivery. Month-end meant an afternoon of adding up, and one bad addition is money lost or an invoice that has to be reissued.",
      "Una autónoma del transporte factura a una empresa cada mes. Veintiuna jornadas escritas a mano: una fecha, una ruta y a veces una segunda entrega. Fin de mes era una tarde de sumar, y una suma mal hecha es dinero perdido o una factura que hay que rehacer.")}</p>

    <div class="numeros sube">
      <div><span class="spec">{t("Invoice total","Total de la factura")}</span><div class="dato">{euros(5574)}</div></div>
      <div><span class="spec">{t("Difference vs. by hand","Diferencia con la de mano")}</span><div class="dato">{euros(0)}</div></div>
      <div><span class="spec">{t("Time it now takes","Lo que tarda ahora")}</span><div class="dato">{t("1 minute","1 minuto")}</div></div>
    </div>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("Why it was hard","Por qué era difícil")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "Nobody writes down “Barcelona, 215 €, VAT 21%, withholding 1%”. They write <b>“1 BCN”</b> in a notebook. Making the invoice meant translating, every month, and the translation is where the mistakes live.",
      "Nadie apunta «Barcelona, 215 €, IVA 21 %, retención 1 %». Se apunta <b>«1 BCN»</b> en una libreta. Hacer la factura exigía traducir, cada mes, y en la traducción es donde viven los errores.")}</p>
    <p class="guia sube" style="margin-top:16px">{t(
      "Two rates depending on the destination, extras charged separately, and destinations whose names lie: in August, one route with “BCN” in it was charged as an outside route, and another without it was charged as Barcelona. <b>The system proposes the rate but never assumes it</b>: anything it guessed is flagged for review, and the money is confirmed by a person.",
      "Dos tarifas según el destino, los extras aparte, y destinos cuyo nombre miente: en agosto, una ruta con «BCN» en el nombre se cobró como externa, y otra sin él se cobró como Barcelona. <b>El sistema propone la tarifa pero no la da por buena</b>: lo que ha supuesto queda marcado para revisar, y el dinero lo confirma una persona.")}</p>
  </div>
</section>

<section class="papel-sec">
  <div class="env">
    <h2 class="sube">{t("What it does now","Lo que hace ahora")}</h2>
    <div class="pasos sube" style="margin-top:32px">
      <div class="paso"><span class="n">01</span><div>
        <h3>{t("She sends a photo of the notebook","Manda una foto de la libreta")}</h3>
        <p>{t("One photo at the end of the month, not a message every day.",
          "Una foto a fin de mes, no un mensaje cada día.")}</p></div></div>
      <div class="paso"><span class="n">02</span><div>
        <h3>{t("It shows what it read, line by line","Enseña lo que ha leído, línea por línea")}</h3>
        <p>{t("Including the lines it could not read. It saves nothing until she says yes.",
          "Incluidas las que no ha sabido leer. No guarda nada hasta que ella dice que sí.")}</p></div></div>
      <div class="paso"><span class="n">03</span><div>
        <h3>{t("The invoice comes out as a PDF","Sale la factura en PDF")}</h3>
        <p>{t("With its series number, its VAT and its withholding. In August it came out identical, to the cent, to the one issued by hand.",
          "Con su número de serie, su IVA y su retención. En agosto salió idéntica, al céntimo, a la que se emitió a mano.")}</p></div></div>
    </div>
    <div class="aviso-demo sube">{t(
      "<b>This is the only real proof on this site.</b> The figures are from an actual August 2026 invoice; the client's tax details are covered. Everything else you will see here is an honest demo and says so on its own page.",
      "<b>Esta es la única prueba real de este sitio.</b> Las cifras son de una factura de agosto de 2026; los datos fiscales del cliente están tapados. Todo lo demás que verás aquí es una demo honesta y lo dice en su propia página.")}</div>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="precios.html">{t("250 € + 20 € a month","250 € + 20 € al mes")}</a>
      <a class="boton" href="mailto:{CORREO}">{t("Talk to me","Hablamos")}</a>
    </div>
  </div>
</section>
</main>
""", CSS_RESTO)

pagina("panel-demo.html",
  t("A dashboard, demonstrated — James J Projects","Un panel, demostrado — James J Projects"),
  t("How many people looked you up and how many called. Demonstration figures, labelled as such.",
    "Cuánta gente te ha buscado y cuántos han llamado. Cifras de demostración, marcadas como tales."),
f"""
<main id="principal">
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("Whether it is<br>working","Si está<br>funcionando")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "A website you cannot measure is an expense. One you can measure is a decision: you know whether it was worth it, and you know which month to push. One screen, no jargon.",
      "Una web que no puedes medir es un gasto. Una que sí, es una decisión: sabes si valió la pena y sabes qué mes apretar. Una pantalla y sin palabras raras.")}</p>

    <div class="numeros sube">
      <div><span class="spec">{t("Looked you up in 12 weeks","Te han buscado en 12 semanas")}</span><div class="dato">{num(1284)}</div></div>
      <div><span class="spec">{t("Called from the profile","Han llamado desde la ficha")}</span><div class="dato">96</div></div>
      <div><span class="spec">{t("Asked for directions","Han pedido cómo llegar")}</span><div class="dato">212</div></div>
    </div>

    <figure class="serie sube" style="margin:0">
      <div class="barras" aria-hidden="true"><i style="height:62.6%;animation-delay:0ms"></i><i style="height:69.5%;animation-delay:34ms"></i><i style="height:67.2%;animation-delay:68ms"></i><i style="height:74.0%;animation-delay:102ms"></i><i style="height:79.4%;animation-delay:136ms"></i><i style="height:75.6%;animation-delay:170ms"></i><i style="height:85.5%;animation-delay:204ms"></i><i style="height:90.1%;animation-delay:238ms"></i><i style="height:81.7%;animation-delay:272ms"></i><i style="height:96.2%;animation-delay:306ms"></i><i class="cima" style="height:100.0%;animation-delay:340ms"></i><i style="height:98.5%;animation-delay:374ms"></i></div>
      <div class="eje">
        <span class="spec">{t("12 weeks ago","Hace 12 semanas")}</span>
        <span class="spec">{t("This week","Esta semana")}</span>
      </div>
      <figcaption class="nota">{t(
        "Searches per week. The twelve bars add up to the " + num(1284) + " above; the tallest, week 11, is when the new photos went up. Read the exact figures in the table below.",
        "Búsquedas por semana. Las doce barras suman las " + num(1284) + " de arriba; la más alta, la semana 11, es cuando se subieron las fotos nuevas. Las cifras exactas, en la tabla de abajo.")}</figcaption>
      <table class="oculto"><caption>{t("Searches per week","Búsquedas por semana")}</caption>
        <thead><tr><th>{t("Week","Semana")}</th><th>{t("Searches","Búsquedas")}</th></tr></thead>
        <tbody><tr><td>1</td><td>82</td></tr><tr><td>2</td><td>91</td></tr><tr><td>3</td><td>88</td></tr><tr><td>4</td><td>97</td></tr><tr><td>5</td><td>104</td></tr><tr><td>6</td><td>99</td></tr><tr><td>7</td><td>112</td></tr><tr><td>8</td><td>118</td></tr><tr><td>9</td><td>107</td></tr><tr><td>10</td><td>126</td></tr><tr><td>11</td><td>131</td></tr><tr><td>12</td><td>129</td></tr></tbody></table>
    </figure>

    <figure class="embudo sube" style="margin:0">
      <figcaption class="spec" style="margin-bottom:6px">{t(
        "Of everyone who looked you up, in 12 weeks",
        "De todos los que te buscaron, en 12 semanas")}</figcaption>
      <div class="paso-e">
        <div class="fila-e"><span class="qui">{t("Looked you up","Te buscaron")}</span>
          <span class="cifra">{num(1284)}<small>100%</small></span></div>
        <div class="via" aria-hidden="true"><i style="width:100%"></i></div>
      </div>
      <div class="paso-e">
        <div class="fila-e"><span class="qui">{t("Asked for directions","Pidieron cómo llegar")}</span>
          <span class="cifra">212<small>16,5%</small></span></div>
        <div class="via" aria-hidden="true"><i style="width:16.5%"></i></div>
      </div>
      <div class="paso-e">
        <div class="fila-e"><span class="qui">{t("Called you","Te llamaron")}</span>
          <span class="cifra">96<small>7,5%</small></span></div>
        <div class="via" aria-hidden="true"><i style="width:7.5%"></i></div>
      </div>
      <figcaption class="nota" style="margin-top:14px">{t(
        "Seven and a half out of every hundred who find you pick up the phone. That is the number worth pushing, and the only one you can act on.",
        "Siete de cada cien de los que te encuentran cogen el teléfono. Ese es el número que merece la pena mover, y el único sobre el que se puede actuar.")}</figcaption>
    </figure>

    <div class="aviso-demo sube">{t(
      "<b>The Bar Marina does not exist and these figures are invented.</b> They are here to show the format, not to boast about results. When it is your business they will be yours, and they will come out of your own Google profile.",
      "<b>El «Bar Marina» no existe y estas cifras son inventadas.</b> Están aquí para enseñar el formato, no para presumir de resultados. Cuando sea tu negocio serán las tuyas y saldrán de tu ficha de Google.")}</div>
  </div>
</section>

<section class="plate">
  <span class="reticula" aria-hidden="true"></span>
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <div class="env">
    <h2 class="sube">{t("Where the<br>numbers come from","De dónde salen<br>los números")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "Straight out of Google's own Business Profile statistics, and out of the site itself. Nothing is estimated and nothing is modelled: if a number cannot be counted, it does not appear on the screen.",
      "Directamente de las estadísticas del Perfil de Negocio de Google y de la propia web. Nada está estimado ni modelado: si un número no se puede contar, no sale en la pantalla.")}</p>
    <p class="guia sube" style="margin-top:16px">{t(
      "It arrives once a month, in an email you can read in thirty seconds. If a month goes badly, the email says so.",
      "Llega una vez al mes, en un correo que se lee en treinta segundos. Si un mes va mal, el correo lo dice.")}</p>
    <div class="acciones sube">
      <a class="boton boton--lleno" href="precios.html">{t("30–50 € a month","30–50 € al mes")}</a>
      <a class="boton" href="index.html">{t("Back to the start","Volver al principio")}</a>
    </div>
  </div>
</section>
</main>
""", CSS_RESTO)
