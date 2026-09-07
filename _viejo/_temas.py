#!/usr/bin/env python3
"""Cada demo lleva su propio tema. Se aplica DESPUÉS de generar, sobrescribiendo
variables: así la casa (index.html) no se toca y las demos enseñan variedad."""
import pathlib, re
BASE = pathlib.Path(__file__).parent

TEMAS = {
 # precios.html deja de ser una muestra de estilo: habla de MI dinero y de mis
 # condiciones, así que lleva mi identidad, no un tema prestado.
 "precios.html": dict(
   nombre="Editorial (la casa)",
   fuentes="Oswald:wght@300;400;500;600&family=Hanken+Grotesk:wght@300;400;500;600;700",
   display='"Oswald","Arial Narrow",sans-serif', texto='"Hanken Grotesk",-apple-system,sans-serif',
   h1="clamp(34px,6.4vw,88px)", h2="clamp(30px,4.6vw,58px)", lh=".94", casa=True,
   vars="""--fondo:#f2f2f0; --superficie:#fff; --hueco:#eaeae7; --borde:#0d0d0f; --borde-fino:#d8d7d3;
   --tinta:#0d0d0f; --tinta-2:#4a4a50; --tinta-3:#8a8a92;
   --naranja:#fe4a23; --fuego:linear-gradient(104deg,#fe4a23,#ff812e); --naranja-piel:#ffeae4;
   --p-azul:#2563eb; --p-verde:#007d55; --menta:#4edea3; --verde-piel:#e8f6ef;"""),

 "carta-nfc.html": dict(
   nombre="Editorial (la casa)",
   fuentes="Oswald:wght@300;400;500;600&family=Hanken+Grotesk:wght@300;400;500;600;700",
   display='"Oswald","Arial Narrow",sans-serif', texto='"Hanken Grotesk",-apple-system,sans-serif',
   h1="clamp(34px,6.4vw,88px)", h2="clamp(30px,4.6vw,58px)", lh=".94", casa=True,
   vars="""--fondo:#f2f2f0; --superficie:#fff; --hueco:#eaeae7; --borde:#0d0d0f; --borde-fino:#d8d7d3;
   --tinta:#0d0d0f; --tinta-2:#4a4a50; --tinta-3:#8a8a92;
   --naranja:#fe4a23; --fuego:linear-gradient(104deg,#fe4a23,#ff812e); --naranja-piel:#ffeae4;
   --p-azul:#2563eb; --p-verde:#007d55; --menta:#4edea3; --verde-piel:#e8f6ef;"""),

 "ficha-google.html": dict(
   nombre="Azul señal", fuentes="Instrument+Serif:ital@0;1&family=Public+Sans:wght@300;400;500;600;700",
   display='"Instrument Serif",Georgia,serif', texto='"Public Sans",-apple-system,sans-serif',
   h1="clamp(46px,8.5vw,104px)", h2="clamp(32px,5.2vw,58px)", lh="1.0",
   vars="""--fondo:#f6f8fb; --superficie:#fff; --hueco:#e8edf5; --borde:#d6dfec; --borde-fino:#e4eaf3;
   --tinta:#0e1520; --tinta-2:#4a5666; --tinta-3:#828d9c;
   --naranja:#1a5fd6; --fuego:linear-gradient(104deg,#1a5fd6,#4a8cff); --naranja-piel:#e3edfd;"""),

 "caso-factura.html": dict(
   nombre="Documento", fuentes="Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700&family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,600",
   display='"Bricolage Grotesque",Helvetica,sans-serif', texto='"Newsreader",Georgia,serif',
   h1="clamp(42px,7.6vw,92px)", h2="clamp(30px,4.8vw,54px)", lh=".98",
   vars="""--fondo:#ecf0f1; --superficie:#fff; --hueco:#dfe6e8; --borde:#cdd8db; --borde-fino:#dde5e7;
   --tinta:#0f1b26; --tinta-2:#455a63; --tinta-3:#7d8f96;
   --naranja:#0f6e6e; --fuego:linear-gradient(104deg,#0f6e6e,#1d9c95); --naranja-piel:#dcefee;"""),

 "panel-demo.html": dict(
   nombre="Índigo", fuentes="Sora:wght@400;600;700&family=Manrope:wght@300;400;500;600;700",
   display='"Sora",-apple-system,sans-serif', texto='"Manrope",-apple-system,sans-serif',
   h1="clamp(38px,6.4vw,78px)", h2="clamp(27px,4.2vw,46px)", lh="1.02",
   vars="""--fondo:#f1f1f7; --superficie:#fff; --hueco:#e6e6f0; --borde:#d8d8e6; --borde-fino:#e6e6f0;
   --tinta:#15141d; --tinta-2:#4f4d63; --tinta-3:#87849c;
   --naranja:#5b53e8; --fuego:linear-gradient(104deg,#5b53e8,#8b82ff); --naranja-piel:#e8e6fd;
   --p-azul:#c2600a; --p-verde:#0e9384;"""),
}

# Lo que solo lleva la página de la casa: titulares en mayúsculas, rótulos muy
# espaciados con su línea, y esquinas rectas en vez de redondeadas.
EDITORIAL = """
  h1,h2{ text-transform:uppercase; }
  .rotulo{ font-family:var(--mono); font-size:10px; font-weight:600; letter-spacing:.28em;
    text-transform:uppercase; display:flex; align-items:center; gap:12px; }
  .rotulo::after{ content:""; flex:1; height:1px; background:var(--borde-fino); }
  /* En la cabecera hay DOS rótulos en la misma fila: si los dos estiran su
     línea, la del primero tacha al segundo. Ahí no lleva línea ninguno. */
  .hilo .rotulo::after{ display:none; }
  /* _estilo.css pinta `.hilo span:last-child` como barra de 2px con el
     degradado, contando con que el último span sea el hilo. Aquí el último es
     el SEGUNDO rótulo, y al darle display:flex la altura pasó a aplicarle y lo
     aplastaba bajo la barra naranja. Se le devuelve su caja. */
  .hilo .rotulo{ height:auto!important; background:none!important; flex:0 0 auto; }
  .hilo{ display:flex; align-items:center; gap:14px; }
  .hilo > span:not(.rotulo){ flex:1; height:1px; background:var(--borde-fino);
    border-radius:0; }
  /* La tarjeta verde venía del tema oliva, que ya no es esta página. */
  .b-verde{ background:var(--naranja-piel); border:1px solid var(--borde); }
  .b-verde .rotulo,.b-verde h3,.b-verde .precio,.b-verde .precio small,
  .b-verde p,.b-verde .listado li{ color:var(--tinta)!important; }
  .b-verde .listado{ border-color:var(--borde-fino)!important; }
  .b-verde .listado li::before{ background:var(--naranja)!important; }
  .bento > *{ border-radius:0; }
  .b-claro,.b-papel,.b-negro,.b-verde{ border:1px solid var(--borde); }
  .boton{ border-radius:0; font-family:var(--mono); font-size:12px; font-weight:600;
    letter-spacing:.16em; text-transform:uppercase; }
  .pil{ border-radius:0; }
"""

for archivo, t in TEMAS.items():
    p = BASE/archivo
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">',
      f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={t["fuentes"]}&family=IBM+Plex+Mono:wght@400;500;600&display=swap">', s)
    s = s.replace("</style>", f"""
  /* ── Tema «{t['nombre']}» · solo esta página ── */
  :root{{ {t['vars']}
    --display:{t['display']}; --texto:{t['texto']}; }}
  h1{{ font-size:{t['h1']}; line-height:{t['lh']}; letter-spacing:-.025em; }}
  h2{{ font-size:{t['h2']}; line-height:{t['lh']}; letter-spacing:-.02em; }}
  .barra .marca{{ font-size:15px; letter-spacing:-.01em; }}
  .precio,.grandota,.aguja .gran{{ letter-spacing:-.04em; }}
  {EDITORIAL if t.get('casa') else ''}
</style>""", 1)
    p.write_text(s, encoding="utf-8")
    print(f"{archivo:24} → {t['nombre']}")
