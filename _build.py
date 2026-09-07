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

FUENTES = ("https://fonts.googleapis.com/css2?"
  "family=Oswald:wght@300;400;500;600"
  "&family=Hanken+Grotesk:wght@300;400;500;600;700"
  "&family=IBM+Plex+Mono:wght@400;500;600&display=swap")

# ── Menú ───────────────────────────────────────────────────────────────
NAV = [
  ("index.html",        {"en":"Home",           "es":"Inicio"}),
  ("precios.html",      {"en":"Pricing",        "es":"Precios"}),
  ("carta-nfc.html",    {"en":"Menu on the table","es":"Carta en la mesa"}),
  ("ficha-google.html", {"en":"Google profile",  "es":"Ficha de Google"}),
  ("caso-factura.html", {"en":"Case",            "es":"Un caso"}),
  ("panel-demo.html",   {"en":"Dashboard",       "es":"Panel"}),
]

def t(en, es):
    """Un texto en los dos idiomas."""
    return en if IDIOMA == "en" else es

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

const btn=document.getElementById('menuBtn'),panel=document.getElementById('menuPanel');
if(btn&&panel){btn.addEventListener('click',()=>{
  const abierto=btn.getAttribute('aria-expanded')==='true';
  btn.setAttribute('aria-expanded',String(!abierto));panel.hidden=abierto;});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden){
    btn.setAttribute('aria-expanded','false');panel.hidden=true;btn.focus();}});}
"""

def barra(actual):
    enlaces = "".join(
      f'<a class="solo-ancho" href="{h}"{" aria-current=\'page\'" if h==actual else ""}>{d[IDIOMA]}</a>'
      for h, d in NAV if h != actual or True)
    movil = "".join(f'<a href="{h}">{d[IDIOMA]}</a>' for h, d in NAV)
    return f"""
<nav class="barra" aria-label="{t('Main','Principal')}">
  <a class="marca" href="index.html">James J Projects</a>
  {enlaces}
  <a class="cta" href="mailto:{CORREO}">{t('Talk to me','Hablamos')}</a>
  <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menuPanel"
    aria-label="{t('Open the menu','Abrir el menú')}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
      stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
  </button>
</nav>
<div class="menu-panel" id="menuPanel" hidden>{movil}
  <a href="mailto:{CORREO}">{t('Talk to me','Hablamos')}</a></div>"""

PIE = f"""
<footer class="pie">
  <div class="env">
    <div class="pie-fila">
      <span class="marca-pie">James J Projects</span>
      <span class="spec">{t('Barcelona and Hamburg · remote','Barcelona y Hamburgo · en remoto')}</span>
    </div>
    <p class="spec pie-nota">{t(
      'Hand-built. No template, no framework, nothing loaded from a third party except the fonts.',
      'Hecho a mano. Sin plantilla, sin framework y sin nada de terceros salvo las tipografías.')}</p>
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FUENTES}">
<style>
{SISTEMA}
{CHASIS}
{css_extra}
</style>
</head>
<body>
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
.barra{position:fixed;z-index:50;top:16px;left:50%;transform:translateX(-50%);
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
.menu-btn{display:none;background:none;border:0;padding:8px;cursor:pointer;
  color:var(--tinta)}
.menu-btn svg{width:21px;height:21px;display:block}
.menu-panel{position:fixed;z-index:49;top:66px;left:50%;transform:translateX(-50%);
  width:calc(100vw - 32px);max-width:420px;background:var(--blanco);
  border:1px solid var(--hilo);padding:8px;display:grid}
.menu-panel a{font-family:var(--mono);font-size:12px;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:var(--tinta);
  text-decoration:none;padding:14px 16px;border-bottom:1px solid var(--hilo)}
.menu-panel a:last-child{border-bottom:0}
@media(max-width:1080px){.barra .solo-ancho{display:none}.menu-btn{display:block}}
@media(min-width:1081px){.menu-panel{display:none!important}}
@media(hover:none){.barra a:not(.marca):hover{background:none;color:var(--tinta-2)}}

.pie{border-top:1px solid var(--tinta);padding:34px 0 54px;margin-top:0}
.pie-fila{display:flex;justify-content:space-between;align-items:baseline;
  gap:20px;flex-wrap:wrap}
.marca-pie{font-family:var(--display);font-size:20px;text-transform:uppercase}
.pie-nota{margin-top:16px;letter-spacing:.14em;line-height:1.9}

/* La portada: la única que empieza pegada arriba */
.portada{padding:132px 0 0}
@media(max-width:760px){.portada{padding-top:104px}}
"""

# ═══════════════════════════ 1. PORTADA ═══════════════════════════════
CSS_HOME = """
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

.firma{margin-top:32px;display:grid;gap:11px;max-width:38rem;
  border-left:1px solid var(--fuego);padding-left:18px;
  animation:aparecer 560ms var(--entrada) 300ms both}
@keyframes aparecer{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.cupo{display:inline-flex;align-items:center;gap:10px;margin-top:24px;
  font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;border:1px solid var(--tinta);padding:10px 17px;
  animation:aparecer 560ms var(--entrada) 380ms both}
.cupo i{width:7px;height:7px;border-radius:50%;background:var(--verde);flex:0 0 auto}
@media(prefers-reduced-motion:no-preference){
  .cupo i{animation:latir 2.6s var(--curva) infinite}
  @keyframes latir{0%,100%{box-shadow:0 0 0 3px rgba(0,125,85,.22)}
                   50%{box-shadow:0 0 0 7px rgba(0,125,85,.05)}}}
.acciones{animation:aparecer 560ms var(--entrada) 460ms both}

/* Las cantidades son la interfaz: la tarifa es el objeto más grande de su
   región y los dígitos guardan su sitio. */
.tarifas{display:grid;grid-template-columns:repeat(4,1fr);
  border:1px solid var(--tinta);margin-top:72px}
.tarifas > a{padding:24px 20px 26px;border-right:1px solid var(--tinta);
  text-decoration:none;color:inherit;display:block;
  transition:background var(--rapido) var(--curva)}
.tarifas > a:last-child{border-right:0}
.tarifas > a:hover{background:var(--blanco)}
.tarifas .que{font-size:15px;color:var(--tinta-2);margin-top:12px;font-weight:300;
  max-width:none}
.tarifas .ir{font-family:var(--mono);font-size:10px;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:var(--fuego-texto);
  margin-top:14px;display:block}
@media(hover:none){.tarifas > a:hover{background:transparent}}
@media(max-width:900px){.tarifas{grid-template-columns:1fr 1fr}
  .tarifas > a:nth-child(2){border-right:0}
  .tarifas > a:nth-child(-n+2){border-bottom:1px solid var(--tinta)}}
@media(max-width:540px){.tarifas{grid-template-columns:1fr}
  .tarifas > a{border-right:0;border-bottom:1px solid var(--tinta)}
  .tarifas > a:last-child{border-bottom:0}}

/* Plate: la pieza cromada con su sombra dura y su destello */
.pieza{position:absolute;right:6%;top:50%;
  transform:translateY(-50%) rotate(-8deg);width:184px;height:244px;
  box-shadow:24px 24px 0 rgba(0,0,0,.32);display:none}
@media(min-width:1080px){.pieza{display:block}}
.pieza .chispa{left:52%;top:27%}
.plate{position:relative;overflow:hidden}
.plate .chispa.a{left:12%;top:24%}
.plate .chispa.b{left:33%;bottom:20%;top:auto}
@media(prefers-reduced-motion:no-preference){
  .plate > .chispa{animation:brillar 3.6s var(--curva) infinite}
  .plate > .chispa.b{animation-delay:1.2s}
  @keyframes brillar{0%,74%,100%{opacity:0;transform:scale(.5)}
                     84%{opacity:1;transform:scale(1)}}}

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

.prueba{display:grid;gap:38px;align-items:center;margin-top:20px}
@media(min-width:900px){.prueba{grid-template-columns:.9fr 1.1fr;gap:64px}}
.grandota{font-family:var(--display);font-size:clamp(56px,9vw,124px);line-height:.86;
  letter-spacing:-.02em}
.cero{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:12px;
  font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  border:1px solid var(--fuego-texto);color:var(--fuego-texto);padding:7px 13px}
.ticket{aspect-ratio:3/4;border:1px solid var(--tinta);background:var(--blanco);
  padding:26px;display:grid;align-content:start;gap:9px;
  box-shadow:18px 18px 0 var(--hueco)}
.ticket i{display:block;height:8px;background:var(--hueco)}
.ticket i.corta{width:54%}
.ticket .corte{height:1px;background:var(--tinta);margin:14px 0 4px}
.ticket .total{height:20px;width:44%;background:var(--tinta);margin-left:auto}

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
<main>
<div class="env">
  <header class="portada">
    <h1 class="titular">
      <span class="linea"><i>{t("Found on","Que te")}</i></span>
      <span class="linea"><i>{t("Google.","encuentren")} <span class="apagado">{t("","en Google")}</span></i></span>
      <span class="linea"><i><em class="subrayado">{t("Walked into.","y entren por la puerta")}</em></i></span>
    </h1>
    <div class="firma">
      <span class="spec">James J Benavides</span>
      <p class="guia">{t(
        "I build the website and put the Google profile in order for bars, garages and neighbourhood shops. I work remotely, so it makes no difference where you are.",
        "Hago la web y pongo en orden la ficha de Google de bares, talleres y tiendas de barrio. Trabajo en remoto, así que da igual dónde estés.")}</p>
    </div>
    <div class="cupo"><i></i>{t("Two jobs at a time","Cojo dos encargos a la vez")}</div>
    <div class="acciones">
      <a class="boton boton--lleno" href="mailto:{CORREO}">{t("Ask for a quote","Pedir presupuesto")}</a>
      <a class="boton" href="precios.html">{t("See the prices","Ver los precios")}</a>
    </div>

    <div class="tarifas">
      <a href="ficha-google.html">
        <div class="precio">150–300 €<small>{t("one-off","una vez")}</small></div>
        <h3>{t("Google profile","Ficha de Google")}</h3>
        <p class="que">{t("The first thing anyone sees when they look you up. Usually still shows last summer's hours.",
          "Lo primero que ve quien te busca. Suele tener el horario del verano pasado.")}</p>
        <span class="ir">{t("What it covers →","Qué incluye →")}</span></a>
      <a href="precios.html">
        <div class="precio">400–900 €<small>{t("closed price","precio cerrado")}</small></div>
        <h3>{t("Full website","Web completa")}</h3>
        <p class="que">{t("One page done properly, not six done badly. Written, not filled in.",
          "Una página bien hecha, no seis mal hechas. Escrita, no rellenada.")}</p>
        <span class="ir">{t("What it covers →","Qué incluye →")}</span></a>
      <a href="carta-nfc.html">
        <div class="precio">120 €<small>{t("up to 20 tables","hasta 20 mesas")}</small></div>
        <h3>{t("Menu on the table","Carta en la mesa")}</h3>
        <p class="que">{t("A sticker per table. Tap the phone, the menu opens. Change a price and it changes everywhere.",
          "Una pegatina por mesa. Acercas el móvil y sale la carta. Cambias un precio y cambia en todas.")}</p>
        <span class="ir">{t("See it live →","Verlo funcionando →")}</span></a>
      <a href="caso-factura.html">
        <div class="precio">250 €<small>{t("+ 20 € a month","+ 20 € al mes")}</small></div>
        <h3>{t("Photo to invoice","De la foto a la factura")}</h3>
        <p class="que">{t("Send a photo of the day sheet, get the invoice as a PDF with VAT and withholding done.",
          "Mandas la foto de la libreta y sale la factura en PDF, con IVA e IRPF hechos.")}</p>
        <span class="ir">{t("Read the case →","Leer el caso →")}</span></a>
    </div>
  </header>
</div>

<section class="plate">
  <span class="chispa a" aria-hidden="true"></span>
  <span class="chispa b" aria-hidden="true"></span>
  <span class="pieza cromo" aria-hidden="true"><span class="chispa"></span></span>
  <div class="env">
    <h2 class="sube">{t("A website is not<br>a printed leaflet","Una web no es<br>un folleto")}</h2>
    <p class="guia sube" style="margin-top:26px">{t(
      "A leaflet is printed once and goes stale. A website gets changed on a Tuesday afternoon because you raised the price of the set menu, and by Wednesday it is right. <b>What I hand you can be changed without calling me.</b>",
      "Un folleto se imprime una vez y se queda viejo. Una web se cambia el martes por la tarde porque has subido el menú, y el miércoles ya está bien. <b>Lo que te entrego se puede cambiar sin llamarme.</b>")}</p>
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
      <div class="ticket sube" aria-hidden="true">
        <i></i><i class="corta"></i><i></i><i class="corta"></i><i></i>
        <div class="corte"></div><div class="total"></div>
      </div>
      <div class="sube">
        <span class="spec">{t("August 2026 · a real invoice","Agosto de 2026 · una factura real")}</span>
        <div class="grandota" style="margin-top:14px">5.574,00&nbsp;€</div>
        <div class="cero">{t("0.00 € difference","0,00 € de diferencia")}</div>
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
.tarjeta{border:1px solid var(--tinta);padding:28px;display:grid;
  align-content:start;gap:0}
.rejilla{display:grid;gap:0;border:1px solid var(--tinta);margin-top:14px}
.rejilla > .tarjeta{border:0;border-bottom:1px solid var(--tinta)}
.rejilla > .tarjeta:last-child{border-bottom:0}
@media(min-width:820px){
  .rejilla{grid-template-columns:1fr 1fr}
  .rejilla > .tarjeta{border-bottom:1px solid var(--tinta);
    border-right:1px solid var(--tinta)}
  .rejilla > .tarjeta:nth-child(2n){border-right:0}
  .rejilla > .tarjeta:nth-last-child(-n+2){border-bottom:0}}
.tarjeta h3{margin:16px 0 10px}
.tarjeta .que{color:var(--tinta-2);font-weight:300;font-size:15.5px}
.lista{list-style:none;padding:18px 0 0;margin:18px 0 0;
  border-top:1px solid var(--hilo);display:grid;gap:9px}
.lista li{font-size:14.5px;color:var(--tinta-2);padding-left:17px;position:relative}
.lista li::before{content:"";position:absolute;left:0;top:9px;width:6px;height:6px;
  background:var(--fuego)}
.aviso-t{margin-top:18px;padding-top:16px;border-top:1px solid var(--hilo);
  font-size:13.5px;color:var(--tinta-3);line-height:1.6}
.faq{border-top:1px solid var(--tinta);margin-top:56px}
.faq > div{padding:26px 0;border-bottom:1px solid var(--hilo)}
.faq h3{margin-bottom:10px}
.faq p{color:var(--tinta-2);font-weight:300;font-size:16px}
"""

def tarjeta(precio, unidad, titulo, que, puntos, nota="", destacada=False):
    lis = "".join(f"<li>{x}</li>" for x in puntos)
    return f"""<div class="tarjeta{' destacada' if destacada else ''}">
    <div class="precio">{precio}<small>{unidad}</small></div>
    <h3>{titulo}</h3><p class="que">{que}</p>
    <ul class="lista">{lis}</ul>
    {f'<p class="aviso-t">{nota}</p>' if nota else ''}</div>"""

pagina("precios.html",
  t("Pricing — James J Projects","Precios — James J Projects"),
  t("Closed prices, written down. What each service costs and what it covers.",
    "Precios cerrados y por escrito. Qué cuesta cada servicio y qué incluye."),
f"""
<main>
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("What it costs,<br>and why","Lo que cuesta,<br>y por qué")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "Asking a price and being told <b>“it depends”</b> is the part everyone dreads. Here it is written down. The quote closes before the work starts: what is said is what is paid, with nothing added at the end.",
      "Preguntar el precio y que te digan <b>«depende»</b> es la parte que a todo el mundo le da pereza. Aquí está escrito. El presupuesto se cierra antes de empezar: lo que se dice es lo que se paga, sin extras al final.")}</p>

    <div class="rejilla sube">
      {tarjeta("150–300 €", t("one-off","una vez"), t("Google profile in order","Ficha de Google en condiciones"),
        t("The first thing a customer sees when they look you up. It is usually stuck on hours from two summers ago, with no decent photo.",
          "Lo primero que ve un cliente cuando busca tu negocio. Suele estar con el horario de hace dos veranos y sin una foto decente."),
        [t("Photos, hours and services up to date","Fotos, horarios y servicios al día"),
         t("Written replies to the reviews you owe","Respuesta escrita a las reseñas pendientes"),
         t("I teach you to answer them yourself in ten minutes","Te enseño a contestarlas tú en diez minutos")])}
      {tarjeta("400–900 €", t("closed price","precio cerrado"), t("Full website","Web completa del negocio"),
        t("One page done properly, not six done badly. What you do, where you are, what it costs and how to reach you.",
          "Una página bien hecha, no seis mal hechas. Qué haces, dónde estás, cuánto cuesta y cómo se te llama."),
        [t("Designed for you, no template","Diseño a medida, sin plantilla"),
         t("Copy written, not filled in","Textos escritos, no rellenados"),
         t("Loads fast on a bad connection","Carga rápido aunque haya poca cobertura"),
         t("Shows up on Google, with a WhatsApp button","Aparecer en Google y botón de WhatsApp"),
         t("Domain and hosting sorted","Dominio y alojamiento resueltos"),
         t("Two rounds of changes included","Dos rondas de cambios incluidas")])}
      {tarjeta("120 €", t("up to 20 tables · +3 € each extra","hasta 20 mesas · +3 € por mesa de más"),
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
      {tarjeta("250 €", t("setup, then 20 € a month","montaje, y 20 € al mes"),
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
      {tarjeta("30–50 €", t("a month, no lock-in","al mes, sin permanencia"), t("Keeping it current","Que no se quede vieja"),
        t("Changes to the menu, the prices, the hours and the photos whenever they are needed.",
          "Cambios de carta, de precios, de horarios y de fotos cuando hagan falta."),
        [t("Unlimited changes within 48 hours","Cambios ilimitados en 48 horas"),
         t("Backup and monitoring","Copia de seguridad y vigilancia"),
         t("One note a month on how the site is doing","Un aviso al mes con cómo va la web")])}
      {tarjeta("0 €", t("always included","siempre incluido"), t("What I do not charge for","Lo que no te cobro"),
        t("Before you commit to anything.","Antes de que te comprometas a nada."),
        [t("The first conversation","La primera conversación"),
         t("Telling you what your profile is missing","Decirte qué le falta a tu ficha"),
         t("The written quote","El presupuesto por escrito")])}
    </div>
  </div>
</section>

<section class="plate">
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
  padding:7px;box-shadow:0 18px 42px rgba(0,0,0,.4)}
.movil .pantalla{width:100%;height:100%;background:var(--blanco);overflow:hidden;
  position:relative}
.cartita{position:absolute;inset:0;padding:9px;opacity:0}
.cartita .cab{height:32px;background:var(--fuego);margin-bottom:8px;display:grid;
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

.pasos{border-top:1px solid var(--tinta);margin-top:12px}
.paso{display:grid;grid-template-columns:44px 1fr;gap:20px;align-items:start;
  padding:26px 0;border-bottom:1px solid var(--tinta)}
.paso .n{font-family:var(--display);font-size:30px;line-height:.9;
  color:var(--tinta-3)}
.paso h3{margin-bottom:8px}
.paso p{font-size:15.5px;color:var(--tinta-2);font-weight:300}
@media(max-width:560px){.paso{grid-template-columns:32px 1fr;gap:14px}}
"""

pagina("carta-nfc.html",
  t("The menu, stuck to the table — James J Projects","La carta, pegada en la mesa — James J Projects"),
  t("A sticker on every table opens your live menu. Change a price once and it changes on every table.",
    "Una pegatina en cada mesa abre tu carta. Cambias un precio una vez y cambia en todas."),
f"""
<main>
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
.rot-lado{position:absolute;top:12px;font-family:var(--mono);font-size:9.5px;
  font-weight:600;letter-spacing:.2em;text-transform:uppercase;
  background:var(--tinta);color:var(--papel);padding:4px 9px;z-index:3}
.rot-lado.izq{left:12px}.rot-lado.der{right:12px}
.ficha-g{background:var(--blanco);border:1px solid var(--hilo);padding:18px;
  display:grid;gap:13px;align-content:start}
.antes .ficha-g{border-color:var(--hilo)}
.fila-g{display:flex;align-items:flex-start;justify-content:space-between;
  gap:12px;flex-wrap:wrap}
.tit-g{font-size:18px;font-weight:600;color:#1a0dab;white-space:normal}
.sub-g{font-size:13px;color:var(--tinta-2)}
.chip-g{font-family:var(--mono);font-size:10px;font-weight:600;padding:4px 9px;
  letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}
.chip-g.cerrado{background:#fbe9e6;color:#a3271a}
.chip-g.abierto{background:#e8f6ef;color:var(--verde)}
.fot-g{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.fot-g img,.fot-g i{display:block;width:100%;max-width:100%;min-width:0;
  aspect-ratio:4/3;object-fit:cover;background:var(--hueco)}
.res-g{font-size:12.5px;color:var(--tinta-2)}
.acc-g{display:flex;gap:6px;flex-wrap:wrap}
.acc-g span{font-family:var(--mono);font-size:10px;font-weight:600;
  border:1px solid var(--azul);color:var(--azul);padding:4px 8px;
  letter-spacing:.06em}
.tirador{position:absolute;top:0;bottom:0;left:52%;width:2px;background:var(--tinta);
  z-index:4;cursor:ew-resize}
.tirador::after{content:"";position:absolute;top:50%;left:50%;width:38px;height:38px;
  transform:translate(-50%,-50%);background:var(--tinta);border-radius:50%}
.tirador span{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  z-index:1;color:var(--papel);font-size:13px;font-family:var(--mono)}
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
.aviso-demo{border:1px solid var(--fuego-texto);padding:18px 20px;margin-top:32px;
  font-size:15px;color:var(--tinta-2);font-weight:300}
.aviso-demo b{color:var(--fuego-texto);font-weight:600}
"""

JS_COMPARAR = """
const c=document.querySelector('.comparar');
if(c){const d=c.querySelector('.lado.desp'),t=c.querySelector('.tirador');
let arrastra=false;
const poner=x=>{const r=c.getBoundingClientRect();
  const p=Math.min(96,Math.max(4,((x-r.left)/r.width)*100));
  d.style.clipPath=`inset(0 0 0 ${p}%)`;t.style.left=p+'%';};
const inicio=e=>{arrastra=true;poner((e.touches?e.touches[0]:e).clientX);};
const mover=e=>{if(!arrastra)return;poner((e.touches?e.touches[0]:e).clientX);};
const fin=()=>{arrastra=false;};
c.addEventListener('mousedown',inicio);c.addEventListener('touchstart',inicio,{passive:true});
window.addEventListener('mousemove',mover);window.addEventListener('touchmove',mover,{passive:true});
window.addEventListener('mouseup',fin);window.addEventListener('touchend',fin);
t.setAttribute('tabindex','0');t.setAttribute('role','slider');
t.setAttribute('aria-label','Comparar antes y despues');
t.setAttribute('aria-valuemin','0');t.setAttribute('aria-valuemax','100');
t.setAttribute('aria-valuenow','52');
t.addEventListener('keydown',e=>{
  const actual=parseFloat(t.style.left)||52;
  if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();
    const p=Math.min(96,Math.max(4,actual+(e.key==='ArrowLeft'?-4:4)));
    d.style.clipPath=`inset(0 0 0 ${p}%)`;t.style.left=p+'%';
    t.setAttribute('aria-valuenow',String(Math.round(p)));}});}
"""

def ficha_google(estado, hrs, fotos, resenas, acciones):
    return f"""<div class="ficha-g">
      <div class="fila-g"><div><div class="tit-g">Bar Sant Ramon</div>
        <div class="sub-g">{t("Tapas bar · Viladecans","Bar de tapas · Viladecans")}<br>{hrs}</div></div>
        {estado}</div>
      <div class="fot-g">{fotos}</div>
      <div class="fila-g"><span class="res-g">{resenas}</span><div class="acc-g">{acciones}</div></div>
    </div>"""

pagina("ficha-google.html",
  t("Your Google profile — James J Projects","Tu ficha de Google — James J Projects"),
  t("The profile with the map beside it is the first thing a customer judges. Drag the bar and compare.",
    "La ficha que sale con el mapa al lado es lo primero que juzga un cliente. Mueve la barra y compara."),
f"""
<main>
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("The same profile,<br>before and after","La misma ficha,<br>antes y después")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "<b>Before they reach your website, people see you on Google.</b> That panel with the map beside it is the first thing a customer judges. In eight out of ten neighbourhood businesses it still shows hours from two summers ago and three blurry photos somebody else took.",
      "<b>Antes de entrar en tu web, la gente te ve en Google.</b> Esa ficha, la que sale con el mapa al lado, es lo primero que juzga un cliente. Y en ocho de cada diez negocios de barrio está con el horario de hace dos veranos y tres fotos borrosas hechas por otros.")}</p>
    <p class="spec" style="margin-top:22px;letter-spacing:.16em">{t("Drag the bar","Arrastra la barra")}</p>

    <div class="comparar sube">
      <span class="rot-lado izq">{t("Before","Antes")}</span>
      <span class="rot-lado der">{t("After","Después")}</span>
      <div class="lado antes">{ficha_google(
        f'<span class="chip-g cerrado">{t("Closed","Cerrado")}</span>',
        t("Says closed · opens at 8:00","Dice cerrado · abre a las 8:00"),
        '<img src="img/mal-local.jpg" alt="" width="360" height="270" loading="lazy">'
        '<img src="img/mal-barra.jpg" alt="" width="360" height="270" loading="lazy">'
        '<i></i><i></i>',
        t("6 reviews with no reply","Sin responder a 6 reseñas"), "")}</div>
      <div class="lado desp">{ficha_google(
        f'<span class="chip-g abierto">{t("Open","Abierto")}</span>',
        t("Open · closes at 23:30","Abierto · cierra a las 23:30"),
        '<img src="img/bien-local.jpg" alt="" width="360" height="270" loading="lazy">'
        '<img src="img/bien-barra.jpg" alt="" width="360" height="270" loading="lazy">'
        '<img src="img/bien-plato.jpg" alt="" width="360" height="270" loading="lazy">'
        '<img src="img/bien-tapa.jpg" alt="" width="360" height="270" loading="lazy">',
        t("6 reviews answered","6 reseñas contestadas"),
        f'<span>{t("Call","Llamar")}</span><span>{t("Directions","Cómo llegar")}</span><span>Web</span>')}</div>
      <div class="tirador"><span>◀▶</span></div>
    </div>
    <p class="guia" style="margin-top:20px;font-size:16px">{t(
      "Example business. What changes is not the design: it is that the hours are true, that you took the photos yourself, and that the reviews have been answered.",
      "Negocio de ejemplo. Lo que cambia no es el diseño: es que el horario sea el de verdad, que las fotos las hayas hecho tú y que las reseñas estén contestadas.")}</p>
  </div>
</section>

<section class="plate">
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
      <a class="boton boton--lleno" href="precios.html">150–300 €</a>
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
<main>
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("Twenty-one days<br>in a notebook","Veintiuna jornadas<br>en una libreta")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "A self-employed driver invoices one company every month. Twenty-one working days written by hand: a date, a route, sometimes a second delivery. Month-end meant an afternoon of adding up, and one bad addition is money lost or an invoice that has to be reissued.",
      "Una autónoma del transporte factura a una empresa cada mes. Veintiuna jornadas escritas a mano: una fecha, una ruta y a veces una segunda entrega. Fin de mes era una tarde de sumar, y una suma mal hecha es dinero perdido o una factura que hay que rehacer.")}</p>

    <div class="numeros sube">
      <div><span class="spec">{t("Invoice total","Total de la factura")}</span><div class="dato">5.574,00 €</div></div>
      <div><span class="spec">{t("Difference vs. by hand","Diferencia con la de mano")}</span><div class="dato">0,00 €</div></div>
      <div><span class="spec">{t("Time it now takes","Lo que tarda ahora")}</span><div class="dato">{t("1 minute","1 minuto")}</div></div>
    </div>
  </div>
</section>

<section class="plate">
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
<main>
<section class="papel-sec" style="padding-top:132px">
  <div class="env">
    <h1>{t("Whether it is<br>working","Si está<br>funcionando")}</h1>
    <p class="guia" style="margin-top:26px">{t(
      "A website you cannot measure is an expense. One you can measure is a decision: you know whether it was worth it, and you know which month to push. One screen, no jargon.",
      "Una web que no puedes medir es un gasto. Una que sí, es una decisión: sabes si valió la pena y sabes qué mes apretar. Una pantalla y sin palabras raras.")}</p>

    <div class="numeros sube">
      <div><span class="spec">{t("Looked you up in 12 weeks","Te han buscado en 12 semanas")}</span><div class="dato">1.284</div></div>
      <div><span class="spec">{t("Called from the profile","Han llamado desde la ficha")}</span><div class="dato">96</div></div>
      <div><span class="spec">{t("Asked for directions","Han pedido cómo llegar")}</span><div class="dato">212</div></div>
    </div>

    <div class="aviso-demo sube">{t(
      "<b>The Bar Sant Ramon does not exist and these figures are invented.</b> They are here to show the format, not to boast about results. When it is your business they will be yours, and they will come out of your own Google profile.",
      "<b>El «Bar Sant Ramon» no existe y estas cifras son inventadas.</b> Están aquí para enseñar el formato, no para presumir de resultados. Cuando sea tu negocio serán las tuyas y saldrán de tu ficha de Google.")}</div>
  </div>
</section>

<section class="plate">
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
