# James J Benavides — portfolio

Webs y fichas de Google para negocios locales del Baix Llobregat y Barcelona.

## Cómo está hecho

Cinco páginas HTML estáticas, sin framework, sin paso de compilación y sin una
sola dependencia en el navegador. Las fuentes se cargan de Google Fonts; todo lo
demás va dentro del propio fichero.

| Fichero | Qué es | Tema |
|---|---|---|
| `index.html` | Portada y trabajos | Fuego · Bebas Neue + Outfit |
| `precios.html` | Precios y preguntas frecuentes | Oliva · Archivo Black |
| `ficha-google.html` | El servicio de la ficha | Azul señal · Instrument Serif |
| `caso-factura.html` | Un caso real | Documento · Bricolage Grotesque |
| `panel-demo.html` | Demostración de panel | Índigo · Sora |

Cada página lleva su propia paleta y sus propias tipografías a propósito: el
muestrario de la portada existe para enseñar variedad, no porque falte criterio.

## Volver a generarlo

```bash
python3 _generar.py   # monta las páginas desde la plantilla y _estilo.css
python3 _temas.py     # aplica el tema de color y letra de cada una
```

`index.html` no lo toca ninguno de los dos: se edita a mano.

## Movimiento

Curvas y duraciones medidas sobre el CSS real de las referencias, no de memoria:
`cubic-bezier(.455,.03,.515,.955)` a 600 ms para las apariciones,
`cubic-bezier(.39,.575,.565,1)` a 200 ms para las microinteracciones. Solo se
animan `transform` y `opacity`. Hay bloque de `prefers-reduced-motion` y una red
de seguridad de 3 s por si la pestaña se abre en segundo plano.

## Aviso sobre las cifras

Las cifras del panel de demostración son **inventadas** y están marcadas como
ejemplo en la propia página. Las del caso de la factura son reales; los datos
fiscales del cliente están tapados.
