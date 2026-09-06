#!/usr/bin/env python3
"""Cada demo lleva su propio tema. Se aplica DESPUÉS de generar, sobrescribiendo
variables: así la casa (index.html) no se toca y las demos enseñan variedad."""
import pathlib, re
BASE = pathlib.Path(__file__).parent

TEMAS = {
 "precios.html": dict(
   nombre="Oliva", fuentes="Archivo+Black&family=Archivo:wght@300;400;500;600;700",
   display='"Archivo Black",Impact,sans-serif', texto='"Archivo",-apple-system,sans-serif',
   h1="clamp(40px,7vw,84px)", h2="clamp(28px,4.4vw,50px)", lh=".95",
   vars="""--fondo:#edefe9; --superficie:#fff; --hueco:#e2e5da; --borde:#d6dacb; --borde-fino:#e3e6dc;
   --tinta:#141710; --tinta-2:#4f5545; --tinta-3:#868c78;
   --naranja:#4d7c1f; --fuego:linear-gradient(104deg,#4d7c1f,#7ba838); --naranja-piel:#e8f0d8;"""),

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
</style>""", 1)
    p.write_text(s, encoding="utf-8")
    print(f"{archivo:24} → {t['nombre']}")
