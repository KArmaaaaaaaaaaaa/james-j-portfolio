# La dirección que quiero: aerografía japonesa

Analizada de tres referencias que me gustan (mecha con cadenas de oro, figura
de gabardina en la carretera, y una lámina editorial azul con «BLUE»).

**No identifiqué al autor.** Busqué y no salió; la tercera lleva marca de
Taschen, así que es de algún libro suyo. Se toma el LENGUAJE visual —paleta,
luz, composición, tipografía—, nunca la ilustración: copiar una obra ajena en
un portfolio que presume de «hecho a mano» sería justo lo contrario.

## Lo que hace que se vea así

**1. Un solo azul, plano y saturado.** No hay degradado de cielo ni
atmósfera: es un plano de color liso, cobalto/ultramar, y la figura se recorta
encima. Eso es lo que le da el aire de lámina y no de foto.

**2. La luz es dura y viene de un sitio.** Sombras proyectadas negras y
nítidas, sin difuminar. En la segunda referencia la sombra del suelo es una
mancha negra rotunda, no una degradación.

**3. Cromado y satinado.** Las telas no tienen textura: tienen bandas de
degradado que simulan metal líquido. Blanco puro en el filo, gris azulado en
el pliegue, y salto brusco entre los dos.

**4. Destellos en estrella.** Cuatro o seis puntas, en los puntos de máximo
brillo. Es la firma de la aerografía de los 80 y lo que más «época» aporta.

**5. Un solo acento cálido.** Bermellón o dorado, y siempre en poca cantidad
contra el azul. Nunca dos acentos.

**6. Contrapicado.** La cámara está por debajo. Monumentaliza al sujeto: es
la razón de que parezcan estatuas.

**7. Tipografía: contraste de escala brutal.** En la lámina, «BLUE» ocupa el
ancho entero en una sans pesadísima, y alrededor hay texto de 6 px en columnas
como una ficha técnica. Y el titular va **tono sobre tono**: azul un punto más
claro que el fondo, no blanco.

Ese punto 7 es el que ya tengo: es lo mismo que hace la dirección editorial de
la portada con Oswald y los rótulos de 10 px. Encajan.

## Cómo se lleva a una web sin que se caiga

Lo que se puede hacer con CSS y sin una sola imagen:

| De la lámina | En la web |
|---|---|
| Azul plano | Sección de fondo cobalto, no la web entera: sobre azul saturado el texto largo cansa |
| Cromado | `linear-gradient` de varias paradas con saltos bruscos |
| Destello | Pseudo-elemento con dos barras cruzadas y `blur`, o `conic-gradient` |
| Sombra dura | `box-shadow` sin desenfoque, solo desplazamiento |
| Tono sobre tono | El titular a `color-mix` del fondo, +12 % de claridad |
| Ficha técnica | Los rótulos de 10 px que ya existen, en columna |

Lo que NO se lleva: el aerógrafo de verdad. Una web no puede pintar volumen
con esa suavidad sin usar imágenes, y llenarla de PNG pesados la haría lenta,
que es justo lo que le vendo a un bar. La dirección se sugiere con color,
luz y escala, no imitando la técnica.
