#!/usr/bin/env python3
"""Genera el sitio de James. Una plantilla, cuatro páginas, cero dependencias."""
import pathlib
BASE = pathlib.Path(__file__).parent

CSS = open(BASE/"_estilo.css", encoding="utf-8").read()
JS = r"""
<script>
(function(){
  var els=document.querySelectorAll('.revelar'), c=new Map();
  els.forEach(function(el){ var p=el.parentElement,n=c.get(p)||0; c.set(p,n+1);
    el.style.transitionDelay=Math.min(n,5)*70+'ms'; });
  var o=new IntersectionObserver(function(es){ es.forEach(function(e){
    if(e.isIntersecting){ e.target.classList.add('visible'); o.unobserve(e.target); } }); },
    {threshold:.15,rootMargin:'0px 0px -10% 0px'});
  els.forEach(function(el){ o.observe(el); });
  setTimeout(function(){ els.forEach(function(el){ el.classList.add('visible'); }); },3000);

  // Números que suben. Se entiende sin explicarlo y cuesta un bucle, no 21 animaciones.
  function mil(n){ return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.'); }
    document.querySelectorAll('.contar').forEach(function(n){
    var fin=+n.dataset.a, ini=null, dur=900, hecho=false;
    function paso(t){ if(!ini) ini=t; var p=Math.min((t-ini)/dur,1);
      var e=1-Math.pow(1-p,3);
      n.textContent=mil(Math.round(fin*e));
      if(p<1) requestAnimationFrame(paso); }
    var ob=new IntersectionObserver(function(es){ es.forEach(function(e){
      if(e.isIntersecting && !hecho){ hecho=true; requestAnimationFrame(paso); ob.unobserve(n); } }); },
      {threshold:.4});
    ob.observe(n);
    setTimeout(function(){ if(!hecho){ hecho=true; n.textContent=mil(fin); } },3000);
  });
})();
</script>
"""
NAV = [("index.html","Inicio"),("precios.html","Precios"),
       ("ficha-google.html","Ficha de Google"),("caso-factura.html","Un caso"),
       ("panel-demo.html","Demo")]

def pagina(archivo, titulo, cuerpo, extra_css="", extra_js=""):
    partes=[]
    for i,(h,t) in enumerate(NAV):
        cur = " aria-current='page'" if h==archivo else ""
        oc  = " oculto"
        partes.append(f'<a class="nav{oc}" href="{h}"{cur}>{t}</a>')
    nav="".join(partes)
    html = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}{extra_css}</style>

<nav class="barra">
  <a class="marca" href="index.html">James J Projects</a>
  {nav}
  <a class="cta" href="mailto:jamesjoelbenavides2004@gmail.com">Hablamos</a>
</nav>

{cuerpo}

<footer class="pie"><div class="env">
  <a href="index.html">Inicio</a><a href="precios.html">Precios</a>
  <a href="ficha-google.html">Ficha de Google</a><a href="caso-factura.html">Un caso</a>
  <a href="panel-demo.html">Demo</a>
  <a href="mailto:jamesjoelbenavides2004@gmail.com">jamesjoelbenavides2004@gmail.com</a>
  <span class="der">Barcelona y Hamburgo</span>
</div></footer>
{JS}{extra_js}"""
    (BASE/archivo).write_text(html, encoding="utf-8")
    return archivo, len(html)

# ═══════════════════════ 1. PRECIOS ═══════════════════════
CSS_PRECIOS = """
  .bento{ display:grid; gap:16px; grid-template-columns:repeat(4,1fr); }
  .bento > *{ border-radius:20px; padding:26px; }
  .b-ancho{ grid-column:span 2; } .b-alto{ grid-row:span 2; }
  @media (max-width:900px){ .bento{ grid-template-columns:repeat(2,1fr); } }
  @media (max-width:560px){ .bento{ grid-template-columns:1fr; }
    .b-ancho,.b-alto{ grid-column:auto; grid-row:auto; } }
  .b-claro{ background:var(--superficie); border:1px solid var(--borde-fino); }
  .b-verde{ background:#dcf0a4; border:1px solid #c9e388; }
  .b-papel{ background:#eaf1f1; border:1px solid #cbdcdc; }
  .b-papel .rotulo{ color:#0f6e6e; }
  .b-papel .listado li::before{ background:#0f6e6e; }
  .b-papel .listado{ border-color:#cbdcdc; }
  .b-papel .listado li{ color:#33484f; }
  .precio .mas{ display:block; font-size:16px; font-weight:500;
    letter-spacing:-.01em; margin-top:2px; color:var(--tinta-2); }
  .b-negro{ background:var(--tinta); color:#fff; border:1px solid var(--tinta); }
  .b-negro .rotulo{ color:#8b8890; }
  .precio{ font-family:var(--mono); font-variant-numeric:tabular-nums; font-size:34px;
    font-weight:600; letter-spacing:-.03em; line-height:1.05; margin:14px 0 4px; }
  .precio small{ font-size:12px; font-weight:400; color:var(--tinta-3); letter-spacing:0; }
  .b-negro .precio small{ color:#8b8890; }
  .listado{ list-style:none; padding:16px 0 0; margin:16px 0 0; border-top:1px solid var(--borde-fino);
    display:grid; gap:8px; }
  .b-negro .listado{ border-color:#33323a; }
  .listado li{ font-size:14.5px; color:var(--tinta-2); padding-left:18px; position:relative; }
  .b-negro .listado li{ color:#c9c6cf; }
  .listado li::before{ content:""; position:absolute; left:0; top:8px; width:7px; height:7px;
    border-radius:50%; background:var(--naranja); }
  .b-verde .listado li::before{ background:#3d6b00; }
  .b-verde .listado li{ color:#3f4a2c; } .b-verde .listado{ border-color:#c2dd7c; }
  .pregunta{ border-bottom:1px solid var(--borde); padding:20px 0; }
  .pregunta h3{ margin-bottom:7px; }
  .pregunta p{ color:var(--tinta-2); font-weight:300; max-width:44rem; font-size:15.5px; }
"""
pagina("precios.html","Precios sin depender", f"""
<div class="env">
  <header class="cabeza">
    <div class="hilo carga"><span class="rotulo">Precios</span><span></span>
      <span class="rotulo">Cerrados y por escrito</span></div>
    <h1 class="carga">Lo que cuesta,<br>y por qué</h1>
    <p class="bajada carga"><b>Preguntar el precio y que te digan «depende» es la parte que a todo el mundo le da pereza.</b> Aquí está escrito. El presupuesto se cierra antes de empezar: lo que se dice es lo que se paga, sin extras al final.</p>
  </header>

  <section>
    <div class="bento">
      <div class="b-claro b-ancho revelar">
        <span class="rotulo">Lo más pedido</span>
        <div class="precio">150–300 € <small>una vez</small></div>
        <h3>Ficha de Google en condiciones</h3>
        <p style="font-size:15px;color:var(--tinta-2);font-weight:300;margin-top:8px">Lo primero que ve un cliente cuando busca tu negocio. Suele estar con el horario de hace dos veranos y sin una foto decente.</p>
        <ul class="listado">
          <li>Fotos, horarios y servicios al día</li>
          <li>Respuesta escrita a las reseñas pendientes</li>
          <li>Te enseño a contestarlas tú en diez minutos</li>
        </ul>
      </div>

      <div class="b-verde b-alto revelar">
        <span class="rotulo" style="color:#4a5a2a">El grueso</span>
        <div class="precio" style="color:#26301a">400–900 € <small style="color:#4a5a2a">precio cerrado</small></div>
        <h3 style="color:#26301a">Web completa del negocio</h3>
        <p style="font-size:15px;color:#3f4a2c;font-weight:300;margin-top:8px">Una página bien hecha, no seis mal hechas. Qué haces, dónde estás, cuánto cuesta y cómo se te llama.</p>
        <ul class="listado">
          <li>Diseño a medida, sin plantilla</li>
          <li>Textos escritos, no rellenados</li>
          <li>Carga rápido aunque haya poca cobertura</li>
          <li>Aparecer en Google y botón de WhatsApp</li>
          <li>Dominio y alojamiento resueltos</li>
          <li>Dos rondas de cambios incluidas</li>
        </ul>
      </div>

      <div class="b-negro revelar">
        <span class="rotulo">Opcional</span>
        <div class="precio">30–50 € <small>al mes</small></div>
        <h3>Que no se quede vieja</h3>
        <ul class="listado">
          <li>Cambios ilimitados en 48 h</li>
          <li>Copia de seguridad</li>
          <li>Sin permanencia</li>
        </ul>
      </div>

      <div class="b-claro revelar">
        <span class="rotulo">Siempre incluido</span>
        <div class="precio">0 €</div>
        <h3>Lo que no te cobro</h3>
        <ul class="listado">
          <li>La primera conversación</li>
          <li>Decirte qué le falta a tu ficha</li>
          <li>El presupuesto por escrito</li>
        </ul>
      </div>

      <div class="b-papel b-ancho revelar">
        <span class="rotulo">Para quien factura por jornadas</span>
        <div class="precio" style="color:#123c3c">250 € <small style="color:#4d7373">montaje, una vez</small>
          <span class="mas" style="color:#33484f">y 20 € al mes mientras lo uses</span></div>
        <h3 style="color:#123c3c">De la foto de la libreta a la factura</h3>
        <p style="font-size:15px;color:#33484f;font-weight:300;margin-top:8px">Si trabajas por rutas, por jornadas o por servicios y a fin de mes te toca sentarte a sumar la libreta, esto lo hace por ti. Mandas <b>una foto de la hoja</b> y sale la factura en PDF, con su número de serie, su IVA y su IRPF.</p>
        <ul class="listado">
          <li>Lee la letra a mano y te enseña línea por línea lo que ha entendido, incluidas las que no ha sabido leer</li>
          <li>No emite nada hasta que tú confirmas el dinero</li>
          <li>Tarifas distintas por tipo de servicio, y los extras aparte</li>
          <li>Las fotos de gasoil, peajes y taller se guardan como gasto del mes</li>
          <li>Aviso el día 28 para que no se te pase</li>
          <li>Resumen en CSV para tu gestoría</li>
        </ul>
        <p style="font-size:13.5px;color:#4d7373;font-weight:300;margin-top:16px;border-top:1px solid #cbdcdc;padding-top:14px">No es una asesoría y no te dice qué declarar: hace la cuenta que ya haces tú, sin equivocarse y en un minuto. <a href="caso-factura.html" style="color:#0f6e6e">Un mes real, al céntimo →</a></p>
      </div>

      <div class="b-papel b-ancho revelar">
        <span class="rotulo">Para bares y restaurantes</span>
        <div class="precio" style="color:#123c3c">120 € <small style="color:#4d7373">hasta 20 mesas</small>
          <span class="mas" style="color:#33484f">y 3 € por cada mesa de más</span></div>
        <h3 style="color:#123c3c">La carta, pegada en la mesa</h3>
        <p style="font-size:15px;color:#33484f;font-weight:300;margin-top:8px">Una pegatina en cada mesa. El cliente <b>acerca el móvil</b> y le sale tu carta con fotos, precios y alérgenos. Sin cámara, sin enfocar, sin app. Y cuando subes un precio, lo cambias tú desde el panel y ya está: <b>no hay que reimprimir nada</b>.</p>
        <ul class="listado">
          <li>Pegatina con chip dentro <b>y el código impreso encima</b>: funciona con cualquier móvil, tenga o no la antena</li>
          <li>Aguanta la limpieza diaria y no se despega</li>
          <li>Cambias la carta desde el móvil y cambia en todas las mesas a la vez</li>
          <li>Cartas de temporada sin tirar las viejas a la basura</li>
          <li>Alérgenos siempre al día, que es obligatorio</li>
        </ul>
        <p style="font-size:13.5px;color:#4d7373;font-weight:300;margin-top:16px;border-top:1px solid #cbdcdc;padding-top:14px">Las fotos las haces tú con el móvil: Google rechaza las generadas por ordenador y desde agosto de 2026 el reglamento europeo obliga a etiquetarlas. <a href="https://sitio-demo-bar.jamesjoelbenavides2004.workers.dev/" style="color:#0f6e6e" target="_blank" rel="noopener">Ver una carta de verdad →</a></p>
      </div>

      <div class="b-claro b-ancho revelar">
        <span class="rotulo">Cómo se paga</span>
        <h3 style="margin-top:12px">La mitad al empezar, la mitad cuando te gusta</h3>
        <p style="font-size:15px;color:var(--tinta-2);font-weight:300;margin-top:8px">Ves la web terminada y funcionando antes de pagar el resto, no un boceto. Si a la segunda ronda de cambios no te convence, te devuelvo la primera mitad y no nos debemos nada.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
          <span class="pil pil--naranja">Transferencia</span>
          <span class="pil pil--azul">Bizum</span>
          <span class="pil pil--verde">Factura con IVA</span>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="titulo revelar"><h2>Lo que suelen preguntar</h2></div>
    <div class="revelar">
      <div class="pregunta"><h3>¿Por qué tan barato comparado con una agencia?</h3>
        <p>Porque no hay agencia. No pagas comerciales, ni oficina, ni al que le pasa el trabajo a otro. Trabajo solo y por las tardes, y por eso también tengo un límite: no puedo coger diez webs a la vez.</p></div>
      <div class="pregunta"><h3>¿La web es mía de verdad?</h3>
        <p>Sí. El dominio se pone a tu nombre y las claves quedan en tu mano. Si mañana quieres irte con otro, te vas con todo. No secuestro webs, que es la práctica que hace que tanta gente desconfíe.</p></div>
      <div class="pregunta"><h3>¿Cuánto tarda?</h3>
        <p>Una semana desde que me pasas las fotos y los textos. La ficha de Google, el mismo día. Lo que suele retrasar un encargo no soy yo: es que el material tarda en llegar.</p></div>
      <div class="pregunta"><h3>No tengo fotos buenas del local.</h3>
        <p>Voy y las hago. Va incluido en la web y en la ficha. Con un móvil actual y buena luz sale mejor que la mayoría de las fotos de banco de imágenes.</p></div>
      <div class="pregunta"><h3>¿Y si el cliente no sabe usar la pegatina?</h3>
        <p>La pegatina lleva las dos cosas: el chip para acercar el móvil y el código impreso encima para quien prefiera la cámara. Cualquier móvil de los últimos diez años entra por una vía o por la otra. Y si alguien no quiere ninguna, le sigues sacando la carta de papel: esto quita trabajo, no lo impone.</p></div>
      <div class="pregunta"><h3>Lo de la factura, ¿vale para mi oficio?</h3>
        <p>Vale para cualquiera que cobre por unidades repetidas: rutas, jornadas, servicios a domicilio, horas. Se configura una vez con tus tarifas y tu cliente, y a partir de ahí es mandar la foto. Lo que no cubre es facturar a cien clientes distintos cada mes: para eso ya hay programas y no te voy a vender el mío.</p></div>
      <div class="pregunta"><h3>¿Y si no sé qué poner?</h3>
        <p>Ese es mi trabajo, no el tuyo. De la conversación de veinte minutos salen los textos. Tú cuentas cómo se lo explicas a un cliente en el mostrador y yo lo escribo.</p></div>
    </div>
    <div class="acciones revelar">
      <a class="boton boton--fuego" href="mailto:jamesjoelbenavides2004@gmail.com?subject=Presupuesto%20para%20mi%20negocio">Pedir presupuesto</a>
      <a class="boton boton--linea" href="caso-factura.html">Ver un trabajo hecho</a>
    </div>
  </section>
</div>
""", CSS_PRECIOS)
print("precios.html")

# ═══════════════════════ 2. FICHA DE GOOGLE ═══════════════════════
CSS_FICHA = """
  .comparar{ display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); }
  .tarjeta-ficha{ border-radius:18px; padding:22px; border:1px solid var(--borde-fino); background:var(--superficie); }
  .tarjeta-ficha.mal{ background:var(--rojo-piel); border-color:#f2d3cd; }
  .tarjeta-ficha.bien{ background:var(--verde-piel); border-color:#c9e3d5; }
  .sello-f{ display:inline-flex; align-items:center; gap:7px; font-family:var(--mono); font-size:11px;
    font-weight:600; letter-spacing:.09em; text-transform:uppercase; margin-bottom:14px; }
  .mal .sello-f{ color:var(--rojo); } .bien .sello-f{ color:var(--p-verde); }
  .pto{ width:7px; height:7px; border-radius:50%; background:currentColor; }
  .simula{ background:var(--superficie); border:1px solid var(--borde-fino); border-radius:12px;
    padding:14px 16px; margin-top:14px; }
  .simula .nom{ font-size:17px; font-weight:600; color:#1a0dab; }
  .simula .est{ font-size:13.5px; color:var(--tinta-2); margin-top:3px; }
  .simula .est b{ font-weight:600; }
  .simula .fot{ display:flex; gap:5px; margin-top:10px; }
  .simula .fot i{ width:44px; height:34px; border-radius:5px; background:var(--hueco); display:block; }
  .bien .simula .fot i{ background:linear-gradient(135deg,#d8cfc2,#c2b6a5); }
  .pasos-f{ counter-reset:p; display:grid; gap:0; border-top:1px solid var(--borde); }
  .paso-f{ display:grid; grid-template-columns:64px 1fr; gap:22px; padding:24px 0;
    border-bottom:1px solid var(--borde); }
  .paso-f .n{ font-family:var(--display); font-size:40px; line-height:.9; color:var(--naranja); }
  .paso-f p{ color:var(--tinta-2); font-weight:300; font-size:15.5px; max-width:40rem; margin-top:6px; }
"""
pagina("ficha-google.html","Ficha de Google en condiciones", """
<div class="env">
  <header class="cabeza">
    <div class="hilo carga"><span class="rotulo">Desde 150 €</span><span></span>
      <span class="rotulo">Listo el mismo día</span></div>
    <h1 class="carga">Tu negocio<br>en Google,<br>bien puesto</h1>
    <p class="bajada carga"><b>Antes de entrar en tu web, la gente te ve en Google.</b> Esa ficha, la que sale con el mapa al lado, es lo primero que juzga un cliente. Y en ocho de cada diez negocios de barrio está con el horario de hace dos veranos y tres fotos borrosas hechas por otros.</p>
    <div class="acciones carga">
      <a class="boton boton--fuego" href="mailto:jamesjoelbenavides2004@gmail.com?subject=Mi%20ficha%20de%20Google&body=Hola%20James%2C%20mi%20negocio%20se%20llama%3A%20">Que le eches un ojo, gratis</a>
      <a class="boton boton--linea" href="precios.html">Ver todos los precios</a>
    </div>
  </header>

  <section>
    <div class="titulo revelar"><h2>La diferencia, en la práctica</h2>
      <p>Lo mismo que ve alguien que busca «bar cerca de mí» un sábado a las nueve de la noche.</p></div>
    <div class="comparar">
      <div class="tarjeta-ficha mal revelar">
        <span class="sello-f"><span class="pto"></span>Como suele estar</span>
        <div class="simula">
          <div class="nom">Bar Sant Ramon</div>
          <div class="est">Bar · Viladecans<br><b style="color:#c0392b">Cerrado</b> · abre a las 8:00</div>
          <div class="fot"><i></i><i></i></div>
        </div>
        <p style="font-size:14.5px;color:#7b2317;margin-top:14px">Dice que está cerrado porque el horario es el del verano pasado. Dos fotos que subió un cliente. Sin web, sin carta, sin responder a nadie. <strong>El de al lado se lleva la mesa.</strong></p>
      </div>
      <div class="tarjeta-ficha bien revelar">
        <span class="sello-f"><span class="pto"></span>Como queda</span>
        <div class="simula">
          <div class="nom">Bar Sant Ramon</div>
          <div class="est">Bar de tapas · Viladecans<br><b style="color:var(--p-verde)">Abierto</b> · cierra a las 23:30</div>
          <div class="fot"><i></i><i></i><i></i><i></i></div>
        </div>
        <p style="font-size:14.5px;color:#1f5240;margin-top:14px">Horario real, incluidos festivos. Fotos del local, de la barra y de dos platos. Carta enlazada, botón de llamar y de cómo llegar. <strong>Las reseñas contestadas una a una.</strong></p>
      </div>
    </div>
  </section>

  <section>
    <div class="titulo revelar"><h2>Qué hago exactamente</h2></div>
    <div class="pasos-f revelar">
      <div class="paso-f"><div class="n cifra">01</div><div>
        <h3>Miro tu ficha antes de cobrarte nada</h3>
        <p>Me mandas el nombre del local por correo y te digo qué le falta, punto por punto. Sin coste y sin que contrates nada. Si está bien, te lo digo y ya está.</p></div></div>
      <div class="paso-f"><div class="n cifra">02</div><div>
        <h3>Voy y hago fotos</h3>
        <p>La fachada, la barra, la sala y dos o tres platos o trabajos. Con buena luz y sin postureo. Las fotos de banco de imágenes se notan y restan.</p></div></div>
      <div class="paso-f"><div class="n cifra">03</div><div>
        <h3>Pongo al día lo que se ve</h3>
        <p>Horarios de verdad, festivos incluidos. Categoría correcta, que es lo que decide si sales cuando buscan tu oficio. Servicios, formas de pago, si hay terraza o acceso para sillas.</p></div></div>
      <div class="paso-f"><div class="n cifra">04</div><div>
        <h3>Contesto las reseñas atrasadas</h3>
        <p>Todas, también las malas. Una reseña de una estrella sin respuesta hace más daño que la reseña. Te dejo escritas las que hay y te enseño a contestar las nuevas en diez minutos.</p></div></div>
      <div class="paso-f"><div class="n cifra">05</div><div>
        <h3>Te enseño a mirar si funciona</h3>
        <p>Google te dice gratis cuánta gente te ha buscado, cuántos han pulsado «cómo llegar» y cuántos han llamado. Te enseño dónde está y qué significa. <a href="panel-demo.html">Así se ve</a>.</p></div></div>
    </div>
  </section>

  <section>
    <div class="caja revelar" style="border-left:none">
      <h3 style="font-size:22px;margin-bottom:12px">Lo que no hago, dicho antes de que preguntes</h3>
      <p style="color:var(--tinta-2);font-weight:300;max-width:44rem">No te prometo salir el primero en Google: eso no lo controla nadie y quien te lo prometa te está mintiendo. No te pido las claves del banco ni de Hacienda, nunca. Y no te ato a una cuota: la ficha se paga una vez y se queda tuya, con tu cuenta y tu contraseña.</p>
      <div class="acciones">
        <a class="boton boton--fuego" href="mailto:jamesjoelbenavides2004@gmail.com?subject=Mi%20ficha%20de%20Google">Escríbeme el nombre del local</a>
      </div>
    </div>
  </section>
</div>
""", CSS_FICHA)
print("ficha-google.html")

# ═══════════════════════ 3. CASO: LA FACTURA ═══════════════════════
CUADROS = "".join('<i></i>' for _ in range(21))
TALLY = f'''<div class="jornadas">
  <div class="malla-j" aria-hidden="true">{CUADROS}</div>
  <div class="pie-j">21 jornadas trabajadas en agosto</div>
</div>'''

CSS_CASO = """
  .jornadas{ background:var(--superficie); border:1px solid var(--borde-fino);
    border-radius:18px; padding:26px 26px 22px; }
  .malla-j{ display:grid; grid-template-columns:repeat(7,1fr); gap:9px; max-width:340px; }
  .malla-j i{ display:block; aspect-ratio:1; border-radius:6px; background:var(--naranja);
    opacity:0; transform:scale(.6); }
  .revelar.visible .malla-j i{ animation:brotar 380ms var(--expo) both; }
  .malla-j i:nth-child(7n+1){ animation-delay:0ms }
  .malla-j i:nth-child(7n+2){ animation-delay:45ms }
  .malla-j i:nth-child(7n+3){ animation-delay:90ms }
  .malla-j i:nth-child(7n+4){ animation-delay:135ms }
  .malla-j i:nth-child(7n+5){ animation-delay:180ms }
  .malla-j i:nth-child(7n+6){ animation-delay:225ms }
  .malla-j i:nth-child(7n+7){ animation-delay:270ms }
  @keyframes brotar{ to{ opacity:1; transform:none; } }
  .pie-j{ margin-top:16px; font-family:var(--mono); font-size:12px; color:var(--tinta-3);
    letter-spacing:.04em; }
  .prueba-caja{ display:grid; gap:34px; align-items:center; }
  @media (min-width:880px){ .prueba-caja{ grid-template-columns:1.1fr .9fr; gap:52px; } }
  .grandota{ font-family:var(--display); font-size:clamp(52px,8vw,104px); line-height:.86;
    font-variant-numeric:tabular-nums; }
  .cero{ display:inline-flex; align-items:center; gap:9px; margin-top:14px; font-family:var(--mono);
    font-size:13px; font-weight:600; color:var(--naranja); background:var(--naranja-piel);
    border-radius:999px; padding:7px 15px; }
  .flujo{ display:flex; align-items:stretch; gap:0; overflow-x:auto; padding:4px 0; }
  .etapa{ flex:none; width:172px; background:var(--superficie); border:1px solid var(--borde-fino);
    border-radius:14px; padding:16px; }
  .etapa .rotulo{ display:block; margin-bottom:8px; }
  .etapa p{ font-size:13.5px; color:var(--tinta-2); font-weight:300; }
  .union{ flex:none; width:32px; display:grid; place-items:center; color:var(--tinta-3); }
  .antes-despues{ display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); }
  .ad{ border-radius:16px; padding:22px; }
  .ad-antes{ background:var(--hueco); border:1px solid var(--borde); }
  .ad-desp{ background:var(--tinta); color:#fff; }
  .ad .v{ font-family:var(--mono); font-variant-numeric:tabular-nums; font-size:30px;
    font-weight:600; letter-spacing:-.03em; margin:10px 0 3px; }
  .ad .l{ font-size:14px; color:var(--tinta-2); } .ad-desp .l{ color:#c9c6cf; }
  .ad-desp .rotulo{ color:#8b8890; }
  .lineas{ list-style:none; padding:0; margin:0; display:grid; gap:12px; }
  .lineas li{ display:grid; grid-template-columns:26px 1fr; gap:12px; font-size:15.5px;
    color:var(--tinta-2); font-weight:300; }
  .lineas .m{ font-family:var(--mono); font-size:11px; font-weight:600; color:var(--naranja);
    background:var(--naranja-piel); border-radius:5px; text-align:center; padding:3px 0; margin-top:3px; }
  .lineas b{ color:var(--tinta); font-weight:600; }
"""
pagina("caso-factura.html","De la libreta a la factura", f"""
<div class="env">
  <header class="cabeza">
    <div class="hilo carga"><span class="rotulo">Un caso · agosto 2026</span><span></span>
      <span class="rotulo">Transporte</span></div>
    <h1 class="carga">De la libreta<br>a la factura</h1>
    <p class="bajada carga">Una transportista apuntaba sus jornadas a mano, con su propia taquigrafía: <em>«1 BCN», «4 Calafell + 30»</em>. Cada fin de mes eran dos horas de Excel, un susto con el IRPF y una gestoría persiguiéndola.</p>
  </header>

  <section class="revelar">
    <div class="prueba-caja">
      {TALLY}
      <div>
        <span class="rotulo">La factura de agosto</span>
        <div class="grandota"><span class="contar" data-a="5574">0</span>,00&nbsp;€</div>
        <span class="cero">0,00 € de diferencia</span>
        <p style="margin-top:16px;color:var(--tinta-2);font-weight:300;max-width:30rem">Veintiuna jornadas. La factura que sacó el sistema salió <strong>idéntica al céntimo</strong> a la que se había emitido a mano. Esa comprobación es la única forma honesta de saber que funciona.</p>
      </div>
    </div>
  </section>

  <section>
    <div class="titulo revelar"><h2>El problema no era la factura</h2>
      <p>Era que hacerla exigía traducir. Nadie apunta «Barcelona, 215 €, IVA 21 %, retención 1 %». Se apunta «1 BCN» en una libreta, entre entrega y entrega.</p></div>
    <div class="revelar"><ul class="lineas">
      <li><span class="m">1</span><span><b>Tarifas distintas según destino.</b> Barcelona una cosa, rutas externas otra, y las segundas entregas aparte. Tres precios que hay que aplicar bien veintiuna veces.</span></li>
      <li><span class="m">2</span><span><b>IVA del 21 % y retención de IRPF del 1 %.</b> Uno suma y el otro resta. Equivocarse de signo es la forma más común de emitir mal una factura.</span></li>
      <li><span class="m">3</span><span><b>El plazo no se mueve.</b> La factura sale el día 1. Si el día 1 caía en domingo o había viaje, se hacía tarde y con prisa, que es cuando salen los errores.</span></li>
    </ul></div>
  </section>

  <section>
    <div class="titulo revelar"><h2>Lo que hace ahora</h2>
      <p>El cliente manda una foto. Lo demás pasa solo.</p></div>
    <div class="flujo revelar">
      <div class="etapa"><span class="rotulo">01</span><h3>La foto</h3><p>Una foto de la libreta por WhatsApp. Es toda la participación del cliente.</p></div>
      <div class="union">→</div>
      <div class="etapa"><span class="rotulo">02</span><h3>Leer la letra</h3><p>Se reconoce el texto escrito a mano, en el propio ordenador. Las fotos no salen de ahí.</p></div>
      <div class="union">→</div>
      <div class="etapa"><span class="rotulo">03</span><h3>Traducir</h3><p>«4 Calafell + 30» pasa a cuatro rutas externas y una segunda entrega, con su tarifa.</p></div>
      <div class="union">→</div>
      <div class="etapa"><span class="rotulo">04</span><h3>La factura</h3><p>PDF con numeración de serie, IVA y retención aplicados, y los datos fiscales correctos.</p></div>
      <div class="union">→</div>
      <div class="etapa"><span class="rotulo">05</span><h3>Enviar</h3><p>Sale por WhatsApp, con un aviso el día 25 para que no se le olvide mandar la libreta.</p></div>
    </div>
  </section>

  <section>
    <div class="titulo revelar"><h2>Antes y después</h2></div>
    <div class="antes-despues revelar">
      <div class="ad ad-antes"><span class="rotulo">Antes</span><div class="v">2 h</div>
        <div class="l">de Excel cada fin de mes, con las prisas del día 1</div></div>
      <div class="ad ad-antes"><span class="rotulo">Antes</span><div class="v">Variable</div>
        <div class="l">riesgo de equivocarse en el signo de la retención</div></div>
      <div class="ad ad-desp"><span class="rotulo">Ahora</span><div class="v">1 foto</div>
        <div class="l">todo lo que tiene que hacer el cliente</div></div>
      <div class="ad ad-desp"><span class="rotulo">Ahora</span><div class="v">0,00 €</div>
        <div class="l">de diferencia con la factura hecha a mano</div></div>
    </div>
    <div class="acciones revelar">
      <a class="boton boton--fuego" href="mailto:jamesjoelbenavides2004@gmail.com?subject=Tengo%20un%20papeleo%20repetitivo">Cuéntame tu caso</a>
      <a class="boton boton--linea" href="panel-demo.html">Ver la demo del panel</a>
    </div>
    <p style="margin-top:26px;font-family:var(--mono);font-size:12px;color:var(--tinta-3);max-width:44rem">Los datos fiscales del caso (NIF, IBAN y nombre del cliente) están tapados a propósito. La cifra de la factura y la diferencia de cero son reales.</p>
  </section>
</div>
""", CSS_CASO)
print("caso-factura.html")

# ═══════════════════════ 4. DEMO DEL PANEL ═══════════════════════
import math
CX,CY,R = 150,150,112
def arco(a0,a1):
    def pt(a):
        t=math.radians(180-a); return CX+R*math.cos(t), CY-R*math.sin(t)
    x0,y0=pt(a0); x1,y1=pt(a1)
    grande = 1 if (a1-a0)>180 else 0
    return f"M{x0:.1f} {y0:.1f} A{R} {R} 0 {grande} 1 {x1:.1f} {y1:.1f}"

TOTAL=1470
segs=[("Buscando tu tipo de negocio",892,"var(--p-azul)"),
      ("Buscando tu nombre",412,"var(--naranja)"),
      ("Desde el mapa",166,"var(--p-verde)")]
a=0.0; arcos=[]
for nom,v,col in segs:
    ang=v/TOTAL*180
    arcos.append(f'<path d="{arco(a+1.2, a+ang-1.2)}" stroke="{col}" stroke-width="18" fill="none" stroke-linecap="round"/>')
    a+=ang
ARCOS="".join(arcos)

vis=[84,91,78,96,110,103,128,141,133,156,168,182]
W,H,PT,PB,PL,PR=520,168,12,26,10,10
mx=max(vis)
def X(i): return PL+i*(W-PL-PR)/(len(vis)-1)
def Y(v): return PT+(1-v/mx)*(H-PT-PB)
L=" ".join(("M" if i==0 else "L")+f"{X(i):.1f} {Y(v):.1f}" for i,v in enumerate(vis))
A=L+f" L{X(len(vis)-1):.1f} {H-PB:.1f} L{X(0):.1f} {H-PB:.1f} Z"
PTS="".join(f'<circle class="pt" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="10" fill="transparent" tabindex="0" data-i="{i}" data-v="{v}"/>' for i,v in enumerate(vis))
REJ="".join(f'<line class="rej" x1="{PL}" y1="{Y(mx*f):.1f}" x2="{W-PR}" y2="{Y(mx*f):.1f}"/>' for f in (0,.5,1))

CSS_DEMO = """
  .aviso-demo{ background:#fff5e0; border:1px solid #f2d8a0; border-radius:14px; padding:16px 20px;
    display:flex; gap:14px; align-items:center; flex-wrap:wrap; margin-bottom:26px; }
  .aviso-demo .et{ font-family:var(--mono); font-size:10.5px; font-weight:600; letter-spacing:.11em;
    text-transform:uppercase; color:#7a4a12; background:#ffe3b0; border-radius:5px; padding:4px 9px; }
  .aviso-demo p{ font-size:14.5px; color:#6b4a1c; margin:0; flex:1; min-width:240px; }
  .app{ background:var(--superficie); border:1px solid var(--borde-fino); border-radius:24px;
    padding:24px; box-shadow:0 18px 44px rgba(40,25,15,.07); }
  .app-cab{ display:flex; align-items:center; gap:14px; flex-wrap:wrap; margin-bottom:22px; }
  .app-cab h3{ font-size:24px; font-weight:500; letter-spacing:-.02em; }
  .app-cab .sub{ font-size:14px; color:var(--tinta-3); width:100%; margin-top:-4px; }
  .pestanas{ display:flex; gap:5px; margin-left:auto; flex-wrap:wrap; }
  .pest{ font-size:13.5px; font-weight:500; color:var(--tinta-2); background:var(--fondo);
    border:1px solid var(--borde-fino); border-radius:999px; padding:8px 15px; cursor:default; }
  .pest.on{ background:var(--tinta); color:#fff; border-color:var(--tinta); }
  .malla{ display:grid; gap:16px; grid-template-columns:1fr; }
  @media (min-width:900px){ .malla{ grid-template-columns:320px 1fr 240px; } }
  .panelito{ background:var(--fondo); border:1px solid var(--borde-fino); border-radius:16px; padding:18px; }
  .panelito .tt{ font-size:14px; font-weight:600; margin-bottom:2px; }
  .panelito .st{ font-size:12.5px; color:var(--tinta-3); margin-bottom:14px; }
  .aguja{ position:relative; text-align:center; }
  .aguja svg{ width:100%; max-width:300px; height:auto; overflow:visible; }
  .aguja .centro{ position:absolute; left:50%; top:64%; transform:translate(-50%,-50%); }
  .aguja .gran{ font-family:var(--mono); font-variant-numeric:tabular-nums; font-size:30px;
    font-weight:600; letter-spacing:-.03em; line-height:1; }
  .aguja .peq{ font-size:12.5px; color:var(--tinta-2); margin-top:3px; }
  .leyenda{ display:grid; gap:9px; margin-top:14px; }
  .leyenda div{ display:flex; align-items:center; gap:9px; font-size:13px; }
  .leyenda i{ width:9px; height:9px; border-radius:50%; flex:none; }
  .leyenda .v{ margin-left:auto; font-family:var(--mono); font-variant-numeric:tabular-nums;
    font-weight:600; font-size:13px; }
  .lienzo{ position:relative; }
  .lienzo svg{ display:block; width:100%; height:auto; overflow:visible; }
  .rej{ stroke:var(--borde); stroke-width:1; }
  .area{ fill:rgba(254,74,35,.10); }
  .linea{ fill:none; stroke:var(--naranja); stroke-width:2; stroke-linejoin:round; stroke-linecap:round; }
  .punta{ fill:var(--naranja); stroke:var(--superficie); stroke-width:2; }
  .cruz{ stroke:var(--tinta-3); stroke-width:1; stroke-dasharray:3 3; opacity:0; }
  .eje{ font-family:var(--mono); font-size:10px; fill:var(--tinta-3); }
  .globo{ position:absolute; pointer-events:none; opacity:0; transform:translate(-50%,-118%);
    background:var(--tinta); color:#fff; border-radius:8px; padding:7px 11px; white-space:nowrap;
    font-family:var(--mono); font-size:11.5px; line-height:1.45; z-index:3;
    transition:opacity var(--micro) var(--salida); }
  .cifras{ display:grid; gap:12px; }
  .cifrita{ background:var(--fondo); border:1px solid var(--borde-fino); border-radius:14px; padding:14px 16px; }
  .cifrita .l{ font-size:12.5px; color:var(--tinta-2); }
  .cifrita .v{ font-family:var(--mono); font-variant-numeric:tabular-nums; font-size:24px;
    font-weight:600; letter-spacing:-.03em; margin-top:4px; display:flex; align-items:baseline; gap:9px; }
  .chip{ font-family:var(--mono); font-size:11px; font-weight:600; border-radius:999px; padding:3px 8px; letter-spacing:0; }
  .chip.sube{ background:var(--verde-piel); color:var(--p-verde); }
  .chip.baja{ background:var(--rojo-piel); color:var(--rojo); }
  .cifrita .c{ font-size:11.5px; color:var(--tinta-3); margin-top:3px; }
  .tablita{ margin-top:16px; overflow-x:auto; }
  table{ border-collapse:collapse; width:100%; min-width:560px; }
  th,td{ text-align:left; padding:12px 14px; border-bottom:1px solid var(--borde-fino); font-size:14.5px; }
  th{ font-family:var(--mono); font-size:10.5px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--tinta-3); font-weight:500; }
  tr:last-child td{ border-bottom:none; }
  td .quien{ font-weight:600; } td .que{ font-size:12.5px; color:var(--tinta-3); }
  .marca{ display:inline-flex; align-items:center; gap:7px; font-family:var(--mono); font-size:11px;
    font-weight:600; border-radius:999px; padding:4px 10px; }
  .marca i{ width:6px; height:6px; border-radius:50%; background:currentColor; }
  .m-ok{ background:var(--verde-piel); color:var(--p-verde); }
  .m-pend{ background:#fff0d6; color:var(--p-ambar); }
  .estrellas{ font-family:var(--mono); font-variant-numeric:tabular-nums; font-weight:600; }
"""
JS_DEMO = """
<script>
(function(){
  var caja=document.getElementById('lz'); if(!caja) return;
  var g=document.getElementById('gl'), cz=document.getElementById('cz'),
      pu=document.getElementById('pu'), svg=caja.querySelector('svg'), n=%d;
  caja.querySelectorAll('.pt').forEach(function(p){
    function e(){
      var cx=p.getAttribute('cx'), cy=p.getAttribute('cy'), i=+p.dataset.i, v=+p.dataset.v,
          r=svg.getBoundingClientRect(), c=caja.getBoundingClientRect(), esc=r.width/%d;
      cz.setAttribute('x1',cx); cz.setAttribute('x2',cx); cz.style.opacity=1;
      pu.setAttribute('cx',cx); pu.setAttribute('cy',cy);
      g.innerHTML='<b>'+v+'</b> visitas<br>'+(i===n-1?'esta semana':'hace '+(n-1-i)+' semanas');
      g.style.left=(r.left-c.left+cx*esc)+'px'; g.style.top=(r.top-c.top+cy*esc)+'px'; g.style.opacity=1;
    }
    p.addEventListener('mouseenter',e); p.addEventListener('focus',e);
  });
  caja.addEventListener('mouseleave',function(){ g.style.opacity=0; cz.style.opacity=0; });
})();
</script>
""" % (len(vis), W)

pagina("panel-demo.html","El panel de tu negocio", f"""
<div class="env">
  <header class="cabeza">
    <div class="hilo carga"><span class="rotulo">Demostración</span><span></span>
      <span class="rotulo">Datos de muestra</span></div>
    <h1 class="carga">El panel<br>de tu negocio</h1>
    <p class="bajada carga">Lo que ve un dueño de bar el lunes por la mañana: <b>cuánta gente le ha buscado, qué ha hecho al encontrarle y si va a más o a menos.</b> Sin palabras raras y sin tener que interpretar nada: la respuesta está escrita en la propia frase.</p>
  </header>

  <section>
    <div class="aviso-demo revelar">
      <span class="et">Ejemplo</span>
      <p><strong>El «Bar Sant Ramon» no existe y estas cifras son inventadas.</strong> Están aquí para enseñar el formato, no para presumir de resultados. Cuando sea tu negocio, serán los tuyos y saldrán de tu ficha de Google.</p>
    </div>

    <div class="app revelar">
      <div class="app-cab">
        <div>
          <h3>Buenos días, Ramon</h3>
          <div class="sub">Bar Sant Ramon · Viladecans · últimas 12 semanas</div>
        </div>
        <div class="pestanas">
          <span class="pest on">Resumen</span><span class="pest">Reseñas</span><span class="pest">Fotos</span>
        </div>
      </div>

      <div class="malla">
        <div class="panelito">
          <div class="tt">Cómo te encuentran</div>
          <div class="st">De 1.470 veces que has salido</div>
          <div class="aguja">
            <svg viewBox="0 0 300 172" role="img" aria-label="De 1.470 apariciones, 892 buscando el tipo de negocio, 412 buscando el nombre y 166 desde el mapa">
              {ARCOS}
            </svg>
            <div class="centro"><div class="gran">1.470</div><div class="peq">veces que has salido</div></div>
          </div>
          <div class="leyenda">
            <div><i style="background:var(--p-azul)"></i>Buscando tu tipo de negocio<span class="v">892</span></div>
            <div><i style="background:var(--naranja)"></i>Buscando tu nombre<span class="v">412</span></div>
            <div><i style="background:var(--p-verde)"></i>Desde el mapa<span class="v">166</span></div>
          </div>
        </div>

        <div class="panelito">
          <div class="tt">Cuánta gente te busca</div>
          <div class="st">Visitas a tu ficha, por semana</div>
          <div class="lienzo" id="lz">
            <svg viewBox="0 0 {W} {H}" role="img" aria-label="Las visitas suben de 84 a 182 por semana en doce semanas">
              {REJ}
              <path class="area" d="{A}"/>
              <path class="linea" d="{L}"/>
              <line class="cruz" id="cz" y1="{PT}" y2="{H-PB}"/>
              <circle class="punta" id="pu" r="4.5" cx="{X(len(vis)-1):.1f}" cy="{Y(vis[-1]):.1f}"/>
              <text class="eje" x="{PL}" y="{H-8}">hace 12 sem.</text>
              <text class="eje" x="{W-PR}" y="{H-8}" text-anchor="end">esta semana</text>
              {PTS}
            </svg>
            <div class="globo" id="gl"></div>
          </div>
        </div>

        <div class="cifras">
          <div class="cifrita"><div class="l">Te han llamado</div>
            <div class="v">47 <span class="chip sube">+22 %</span></div>
            <div class="c">frente a las 12 semanas anteriores</div></div>
          <div class="cifrita"><div class="l">Han pedido cómo llegar</div>
            <div class="v">112 <span class="chip sube">+38 %</span></div>
            <div class="c">es la acción más repetida</div></div>
          <div class="cifrita"><div class="l">Nota media</div>
            <div class="v">4,6 <span class="chip baja">−0,1</span></div>
            <div class="c">sobre 38 opiniones</div></div>
        </div>
      </div>

      <div class="tablita">
        <table>
          <thead><tr><th>Reseña</th><th>Nota</th><th>Cuándo</th><th>Contestada</th></tr></thead>
          <tbody>
            <tr><td><span class="quien">Marta G.</span><div class="que">«El menú del día, impecable»</div></td>
              <td class="estrellas">5,0</td><td>hace 2 días</td><td><span class="marca m-ok"><i></i>Sí</span></td></tr>
            <tr><td><span class="quien">Joan P.</span><div class="que">«Tardaron con la comanda»</div></td>
              <td class="estrellas">3,0</td><td>hace 5 días</td><td><span class="marca m-pend"><i></i>Pendiente</span></td></tr>
            <tr><td><span class="quien">Lucía R.</span><div class="que">«La terraza es lo mejor del barrio»</div></td>
              <td class="estrellas">5,0</td><td>hace 1 semana</td><td><span class="marca m-ok"><i></i>Sí</span></td></tr>
            <tr><td><span class="quien">Andrés M.</span><div class="que">«Buen precio, sitio sencillo»</div></td>
              <td class="estrellas">4,0</td><td>hace 2 semanas</td><td><span class="marca m-ok"><i></i>Sí</span></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section>
    <div class="titulo revelar"><h2>De dónde salen estos números</h2>
      <p>De tu ficha de Google, que ya los recoge gratis y casi nadie mira. Yo solo los saco de donde están escondidos y los pongo en una frase que se entiende.</p></div>
    <div class="acciones revelar">
      <a class="boton boton--fuego" href="ficha-google.html">Ver el servicio de la ficha</a>
      <a class="boton boton--linea" href="precios.html">Precios</a>
    </div>
  </section>
</div>
""", CSS_DEMO, JS_DEMO)
print("panel-demo.html")
