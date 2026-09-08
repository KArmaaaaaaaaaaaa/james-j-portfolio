---
name: James J Projects
description: Japanese 80s airbrush over an Apple motion chassis — flat cobalt plates, hard-banded chrome, zero-blur cast shadows, one warm accent.
colors:
  papel: "#f2f2f0"
  blanco: "#ffffff"
  hueco: "#e9e9e6"
  hilo: "#d7d6d2"
  tinta: "#0d0d0f"
  tinta-2: "#4a4a50"
  tinta-3: "#6d6d75"
  cobalto: "#0f3fa8"
  cobalto-hondo: "#0a2c78"
  cobalto-alto: "#6493f7"
  sobre-cobalto: "#e8eeff"
  sobre-cobalto-2: "#a9c0f5"
  hilo-cobalto: "#3a63bd"
  fuego: "#fe4a23"
  fuego-texto: "#c92e0d"
  fuego-fondo: "#b02607"
  verde: "#007d55"
  azul: "#2563eb"
typography:
  display:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(34px, 8.4vw, 112px)"
    fontWeight: 500
    lineHeight: 0.9
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(30px, 5vw, 68px)"
    fontWeight: 500
    lineHeight: 0.94
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(19px, 2vw, 25px)"
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: "-0.005em"
  quantity:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(38px, 5.4vw, 72px)"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.02em"
  quantity-hero:
    fontFamily: "Oswald, Arial Narrow, sans-serif"
    fontSize: "clamp(56px, 9vw, 124px)"
    fontWeight: 500
    lineHeight: 0.86
    letterSpacing: "-0.02em"
  lead:
    fontFamily: "Hanken Grotesk, -apple-system, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif"
    fontSize: "19px"
    fontWeight: 300
    lineHeight: 1.6
  body:
    fontFamily: "Hanken Grotesk, -apple-system, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  note:
    fontFamily: "Hanken Grotesk, -apple-system, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif"
    fontSize: "13.5px"
    fontWeight: 300
    lineHeight: 1.7
  label:
    fontFamily: "IBM Plex Mono, ui-monospace, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.2em"
  action:
    fontFamily: "IBM Plex Mono, ui-monospace, Menlo, monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.16em"
  nav:
    fontFamily: "IBM Plex Mono, ui-monospace, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.12em"
rounded:
  none: "0"
  focus: "2px"
  dot: "50%"
spacing:
  hairline: "1px"
  gutter-sm: "18px"
  gutter: "26px"
  band: "clamp(72px, 9vw, 124px)"
  page-top: "132px"
  measure: "68ch"
  container: "74rem"
components:
  button-primary:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "17px 28px"
  button-primary-hover:
    backgroundColor: "{colors.fuego-fondo}"
    textColor: "{colors.blanco}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "17px 28px"
  button-outline-hover:
    backgroundColor: "{colors.fuego-fondo}"
    textColor: "{colors.blanco}"
  button-primary-on-plate:
    backgroundColor: "{colors.sobre-cobalto}"
    textColor: "{colors.cobalto-hondo}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "17px 28px"
  button-outline-on-plate:
    backgroundColor: "transparent"
    textColor: "{colors.sobre-cobalto}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "17px 28px"
  nav-bar:
    backgroundColor: "rgba(255,255,255,.9)"
    textColor: "{colors.tinta-2}"
    typography: "{typography.nav}"
    rounded: "{rounded.none}"
    padding: "7px 8px 7px 18px"
  nav-link-current:
    backgroundColor: "{colors.hueco}"
    textColor: "{colors.tinta}"
  nav-cta:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    typography: "{typography.nav}"
    padding: "9px 12px"
  card-price:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.none}"
    padding: "28px"
  plate:
    backgroundColor: "{colors.cobalto}"
    textColor: "{colors.sobre-cobalto}"
    rounded: "{rounded.none}"
    padding: "{spacing.band} 0"
  paper-section:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.none}"
    padding: "{spacing.band} 0"
  chip-availability:
    backgroundColor: "transparent"
    textColor: "{colors.tinta}"
    typography: "{typography.nav}"
    rounded: "{rounded.none}"
    padding: "10px 17px"
  skip-link:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    typography: "{typography.nav}"
    rounded: "{rounded.none}"
    padding: "13px 20px"
---

# Design System: James J Projects

## Overview

**Creative North Star: "The Airbrushed Plate"**

The world is Japanese 80s airbrush illustration rendered on an Apple motion
chassis. Airbrush supplies the materials — flat saturated cobalt fields, chrome
rendered as hard bands that cut instead of blending, black cast shadows thrown
with zero blur, four-point sparkles with concave sides at peak highlights — and
Apple supplies the behaviour: measured easing, short durations, transform and
opacity only, nothing that bounces or spins. The two halves are not a blend.
The still image is airbrush; the way it arrives is Apple.

Sections read as plates in a book. A page is a stack of full-bleed bands that
alternate cool paper (#f2f2f0) and flat cobalt (#0f3fa8), each band carrying
the same recurring objects: a rotated chrome piece with its hard shadow, one or
two sparkles, a headline set in condensed uppercase. Rank between bands is
carried by colour inversion, never by type growing. Structure is drawn with
1px hairlines and shared borders rather than with gaps, shadows or radii:
tables of prices, grids of facts and lists of works are all built from cells
that touch. Nothing is rounded except a focus outline and one
slider handle.

Density is high and text is narrow. Prose is capped at a 68ch measure inside a
74rem container while structural grids run the full band, so long-form reading
and full-width evidence coexist without a second layout system. Prices are the
largest object in their region because the product is priced honestly and the
price is the argument. The build refuses the agency landing page: no hero stock
photo, no three-benefit card row, no gradient blur, and no kicker or eyebrow
above any headline — a headline stands alone, and mono labels sit beside content
or under a figure.

**Key Characteristics:**
- Two grounds only: cool paper and flat cobalt, alternating full-bleed.
- Chrome as hard-banded gradient; blends are not chrome.
- Cast shadows: solid black, zero blur, large offset.
- Four-point sparkles with concave sides, never a plain cross.
- One warm accent, never two.
- Everything square; hairlines instead of gaps.
- Condensed uppercase display, humanist grotesque prose, mono for labels only.
- Motion measured from apple.com: transform and opacity, nothing past 560 ms.

## Colors

Two grounds and one flame. Paper is deliberately cool rather than cream — the
plate is a printed sheet, not an old book — and cobalt is a field, not a sky
gradient.

### Primary
- **Cobalt Field** (`{colors.cobalto}`): the inverted band. Full-bleed, negative
  page margins, no gradient, no texture. It is the system's hierarchy device.
- **Deep Cobalt** (`{colors.cobalto-hondo}`): text colour for filled buttons and
  selection on cobalt; the only darker blue, never used as a ground.
- **High Cobalt** (`{colors.cobalto-alto}`): headlines on cobalt, tone on tone.
  It measures 3.07:1 against the field — legible at large-text sizes and still
  unmistakably blue on blue. The earlier #2f60d6 was 1.64:1 and failed.

### Secondary
- **Flame** (`{colors.fuego}`): surface-only vermilion. The rule drawn under the
  last headline phrase, list bullets, the signature's left rule, the NFC scene's
  ripple and menu header. Never text.
- **Flame Text** (`{colors.fuego-texto}`): links, "→" affordances, the zero-
  difference badge, demo-warning borders. 4.83:1 on paper; the surface vermilion
  gives only 3.01:1 and is therefore banned from type.
- **Flame Ground** (`{colors.fuego-fondo}`): every button hover, the selection
  highlight, focus outlines and the browser `accent-color`. Carries white.

### Tertiary
- **Trade Green** (`{colors.verde}`): the availability dot and the "Open" chip in
  the Google-profile comparison.
- **Link Blue** (`{colors.azul}`): the action chips inside the Google profile
  mock only. These are regional colours borrowed from the artefact being
  depicted; they never leave their region.

### Neutral
- **Paper** (`{colors.papel}`): the default page ground.
- **White** (`{colors.blanco}`): raised objects on paper — the ticket, the mobile
  menu panel, the "after" side of the comparison, hover state of price cells.
- **Hollow** (`{colors.hueco}`): the inert fill — placeholder bars, scrollbar
  track, the "before" side, current-nav-item background.
- **Thread** (`{colors.hilo}`): hairline on paper for secondary divisions.
- **Ink** (`{colors.tinta}`): body text, all structural borders, the skip link
  and the filled button.
- **Ink 2** (`{colors.tinta-2}`): supporting prose and nav links at rest.
- **Ink 3** (`{colors.tinta-3}`): the 11px mono spec labels and short notes.
  4.58:1 on paper; it exists at exactly this value because small type needs 4.5.
- **On Cobalt** (`{colors.sobre-cobalto}`) / **On Cobalt 2**
  (`{colors.sobre-cobalto-2}`): body and secondary text inside a cobalt band.
- **Cobalt Thread** (`{colors.hilo-cobalto}`): the hairline inside a cobalt band.

### Named Rules

**The One Flame Rule.** There is one warm accent in the system and never two.
Anything that wants to be "another highlight colour" is either the flame or a
neutral.

**The Flame Splits By Ground Rule.** The vermilion has three values and they are
not interchangeable: `{colors.fuego}` paints surfaces, `{colors.fuego-texto}`
sets type on paper, `{colors.fuego-fondo}` is any ground that carries white.
Never set type in `{colors.fuego}`.

**The Inversion Rule.** Rank is carried by inverting the ground between a paper
section and a cobalt plate. A more important section does not get bigger type,
more weight or a shadow; it gets the other colour.

**The Computed Contrast Rule.** Every text colour in this palette was measured,
not assumed, and two of them exist only because the assumed value failed. A new
text colour ships only with its ratio computed against the ground it sits on:
4.5:1 for anything under 18.66px, 3:1 above it.

**The Regional Accent Rule.** Green and blue exist to render a depicted artefact
(a Google profile, an availability dot). They stay inside that component and
never become page-level accents.

## Typography

**Display Font:** Oswald 400–500 (fallback Arial Narrow) — self-hosted
**Body Font:** Hanken Grotesk 300–600 (fallback -apple-system) — self-hosted
**Label/Mono Font:** IBM Plex Mono 400 and 600 — self-hosted

**Character:** A condensed grotesque shouting in uppercase over a quiet
low-contrast humanist body, with a monospace used strictly as machine
annotation. The pairing reads like a technical sheet for a poster: the display
is loud and tight, the prose is calm and light, and the mono never argues with
either because it is always small and always widely tracked.

All three families are subset to latin and latin-ext and served from `fuentes/`.
The site loads nothing from a third party; the footer says so, and self-hosting
is what makes that true. Latin and latin-ext also cover both shipping languages.

### Hierarchy
- **Display** (Oswald 500, `clamp(34px, 8.4vw, 112px)`, line-height 0.9,
  tracking -0.015em, uppercase): one H1 per page, balanced with `text-wrap`, set
  as three block lines that clip and rise.
- **Headline** (Oswald 500, `clamp(30px, 5vw, 68px)`, line-height 0.94,
  uppercase): the opening of every band, usually two lines split by `<br>`.
- **Title** (Oswald 500, `clamp(19px, 2vw, 25px)`, line-height 1.1, uppercase):
  card, step and row titles.
- **Quantity** (Oswald 500, `clamp(38px, 5.4vw, 72px)`, line-height 1, tracking
  -0.02em): every price. A quantity hero variant (`clamp(56px, 9vw, 124px)`,
  line-height 0.86) is used for the single proof figure and the invoice totals.
- **Lead** (Hanken Grotesk 300, 19px/1.6, ink-2): the paragraph directly under a
  headline. Bold runs inside it are weight 600 in full ink and carry the claim.
- **Body** (Hanken Grotesk 400, 17px/1.6): default page text, capped at 68ch.
- **Supporting** (Hanken Grotesk 300, 15–15.5px): card and row descriptions.
- **Note** (Hanken Grotesk 300, 13.5px/1.7, ink-3, max 56ch): caveats and the
  footer's honesty line. A small *sentence* uses the reading face, not the mono.
- **Label** (IBM Plex Mono 600, 11px, tracking 0.2em, uppercase, ink-3): the
  spec label. Two or three words, no more.
- **Action** (IBM Plex Mono 600, 12px, tracking 0.16em, uppercase): buttons;
  11px/0.12em for nav links, 10–11px/0.16–0.18em for the "→" link affordance.

### Named Rules

**The Headline Stands Alone Rule.** A mono spec label goes beside content or
under a figure. It never sits above a headline as a kicker or eyebrow. If a
headline needs a label to be understood, rewrite the headline.

**The Mono Is Not Prose Rule.** Tracked monospace is legible for two or three
words. A full sentence returns to Hanken Grotesk at 13.5px, even when it is the
smallest text on the page.

**The Quantities Are The Interface Rule.** In any region that states a price, the
price is the largest object in that region and its digits hold their positions
(`font-variant-numeric: tabular-nums` on headings, figures, table cells and
prices). The unit is a mono label under the number, never beside it.

## Layout

A 74rem container with 26px gutters (18px under 640px), and prose capped at a
68ch measure inside it. Cobalt plates and the NFC scene break out to full bleed
with `margin-inline: calc(50% - 50vw)` and re-inset their contents with
`padding-inline: max(26px, calc(50vw - var(--ancho)/2 + 26px))`, so a band is
edge-to-edge while its text stays on the same measure as the paper above it.

Vertical rhythm is banded, not stepped: every section — paper or cobalt — is
`clamp(72px, 9vw, 124px)` of block padding. The first section of every page
starts at 132px (104px under 760px) to clear the floating nav bar. Inside a
band, spacing is small and local (9–38px) and does most of its work through
borders instead of margins.

Structural grids use `gap: 0` and share 1px ink borders. The home price table is
four columns, collapsing 4 → 2 (900px) → 1 (540px) by moving which cell owns
which border. Fact strips are four columns collapsing to two at 760px, the
pricing grid is two columns above 820px and one below, the case figures are
three columns collapsing to one at 700px. Cells never gain a gap when they
collapse; they change which edge carries the hairline.

Named breakpoints as actually used: 430px (buttons stack), 540/560px, 640px
(gutter drop), 700/760px, 820/900px, 1080px (nav collapses to the panel button),
1120px (the cover's chrome plate appears).

## Elevation & Depth

This system has no ambient shadow and no blur. Depth is a cast shadow: an opaque
black offset with zero spread, thrown down and to the right at 45°, exactly as
an airbrush illustration casts a shape onto its ground. The shadow takes the
colour of the ground it falls on — full ink on paper, `rgba(0,0,0,.3)` on
cobalt, because black-on-blue at full opacity reads as a hole. Everything else
that could suggest elevation is done by inversion or by a 1px border.

### Shadow Vocabulary
- **Cast on paper, large** (`box-shadow: 22px 22px 0 var(--tinta)`): the cover's
  chrome plate. Also 14px 14px on the ticket.
- **Cast on cobalt** (`box-shadow: 24px 24px 0 rgba(0,0,0,.32)`; 16px 16px under
  1080px): the chrome piece inside a plate.
- **Cast, small** (`box-shadow: 8px 8px 0 rgba(0,0,0,.3)`): the NFC sticker on
  the cobalt scene.
- **Pulse ring** (`box-shadow: 0 0 0 3px → 0 0 0 7px rgba(0,125,85,.22→.05)`):
  the availability dot only. It is a ring, not depth.

### Named Rules

**The Zero-Blur Rule.** A shadow in this system has no blur radius and no
spread: `Xpx Xpx 0 <opaque colour>`. If a shadow needs blur to look right, the
object is wrong, not the shadow.

**The Shadow Takes Its Ground Rule.** Cast shadows are `var(--tinta)` on paper
and `rgba(0,0,0,.3)` on cobalt. A shadow never carries a colour its ground
would not produce.

**The Flat-Chrome Rule.** Chrome is a `linear-gradient` at 101° with hard,
closely-spaced stops that cut from a dark band straight to white. A smooth
blend is not chrome in this world; it is a gradient, and gradients are refused.

## Shapes

Everything is square. There is no radius scale: `border-radius` appears exactly
three times in the shipped CSS — 2px on the focus outline, 50% on the
availability dot, 50% on the comparison slider handle. Cards, buttons, chips,
plates, panels, the nav bar, the mobile menu and every grid cell have sharp
corners.

Form comes from three recurring silhouettes. The **hairline cell**: a 1px ink
border around a grid whose children share edges and never gap. The **rotated
plate**: a rectangle turned -8°, -6° or +5° with a hard cast shadow, appearing
on the cover as a chrome sheet over a cobalt panel and inside every cobalt band
as a smaller chrome piece bleeding off the edge — on narrow screens it moves to
the corner and runs off the plane rather than hiding. The **four-point sparkle**:
a clip-path star whose sides are pulled inward
(`polygon(50% 0, 54% 46%, 100% 50%, 54% 54%, 50% 100%, 46% 54%, 0 50%, 46% 46%)`)
in white at 0.92 opacity, sized by a `--chispa` custom property.

### Named Rules

**The Concave Sides Rule.** A four-point sparkle has sides that curve inward.
A star drawn with straight sides is a cross, and a cross is not this world.

**The World Lives In The Chassis Rule.** The chrome piece, its cast shadow and
its sparkles are defined on `.plate` in the shared chassis, not on one page. A
motif that appears on a single page is an ornament, not a world.

## Components

### Buttons
- **Shape:** square (0 radius), 1px ink border, `17px 28px` of padding, mono
  uppercase at 12px/0.16em.
- **Flush pairs:** buttons sit in a `.acciones` flex row with `gap: 0`; the
  second button drops its left border so the pair reads as one divided object.
  Under 430px the row becomes a single-column grid, the shared edge moves to the
  left border and the labels centre.
- **Primary:** filled ink on paper (`{components.button-primary}`); on a cobalt
  plate it inverts to on-cobalt fill with deep-cobalt text.
- **Secondary:** transparent with an ink border on paper, on-cobalt border and
  text inside a plate.
- **Hover:** both variants go to flame ground with white text and a flame
  border, over 160 ms. **Active:** `scale(.985)`. On touch devices every hover
  state is reverted to its rest state via `@media(hover: none)`.

### Price Cells and Cards
- Square, 1px ink border, 28px internal padding, content grid with `gap: 0`.
- The price leads (quantity role), then the title, then a light 15.5px
  description, then a bulleted list separated by a thread hairline. Bullets are
  6px flame squares, absolutely positioned — no list glyph.
- The home price table is the same object in table form: four cells sharing ink
  borders, each a whole link, hovering to white with a 240 ms background
  transition, closing with a flame-text "→" affordance.

### Navigation
- A floating capsuleless bar, fixed 16px from the top and centred, on 90% white
  with `backdrop-filter: saturate(180%) blur(16px)` and a thread border. This is
  the only blur in the system and it is a chassis surface, not a shadow.
- Brand in Oswald 19px uppercase; links in mono 11px/0.12em ink-2, hovering to
  ink on hollow. The current page carries `aria-current` and renders in the
  same hollow-plus-ink state as hover.
- The final item is a filled ink CTA that hovers to flame ground.
- Under 1080px all links collapse behind an inline SVG hamburger (stroke 1.8,
  currentColor) that toggles `aria-expanded` and a `hidden` white panel of
  full-width mono rows divided by thread hairlines. Escape closes it and
  returns focus to the button.

### Skip Link
Fixed, centred, mono 11px on ink, parked at `translate(-50%, -160%)` and sliding
into place on `:focus` over 240 ms. It is the first thing the keyboard reaches.

### Before/After Comparison (signature)
Two stacked panels in one grid cell; the "after" side is revealed by
`clip-path: inset(0 0 0 X%)` driven by a 2px ink handle with a 38px ink circle.
Pointer, touch and keyboard all drive the same setter (arrows ±4%, Home 4%,
End 96%), and the handle is a real `role="slider"` that publishes
`aria-valuenow` and a spoken `aria-valuetext`. Corner labels are mono 11px on
ink. It is the one round object in the system and it earns it by being a grip.

### Sparkle and Chrome Piece (signature)
`.chispa` is a positioned four-point star sized by `--chispa` (44–104px as
shipped). `.pieza` is the chrome rectangle carried by every plate: 118×156px
rotated -8° with a 16px cast shadow on narrow screens, 184×244px with a 24px
cast shadow above 1080px, always bleeding past the band's edge.

### Numbered Steps
`.pasos` is an ink-ruled list; each `.paso` is a two-column grid (44px number
track, 20px gap, 32/14 under 560px) with 26px of vertical padding and a hairline
between rows. The number is Oswald 30px in ink-3 — it labels the row from beside
it, never from above it. It lives in the chassis, not in one page's CSS, because
two pages use it.

### Week Series (dashboard)
`.serie` is a twelve-column grid of flat cobalt bars, `align-items: end`, 172px
tall (132px under 560px), joined to the figures panel above it by dropping its
own top border. One bar carries `.cima` in flame — the week the story turns —
and it is the only place a bar changes colour. Bars grow with `scaleY` from a
bottom origin, 520 ms on `--expo`, staggered 34 ms, and the animation is dropped
entirely under reduced motion. The axis is a hairline with a mono label at each
end. The exact figures ship as a real `<table>` in `.oculto` (clip-path inset)
so the chart is data, not decoration; the bars are `aria-hidden`. The twelve
values add up to the headline figure above them: a demonstration still has to
reconcile.

### Cover Plate (`.lamina`, home only)
The home cover's right third is held by a 284×496px chrome plate rotated 5°
over a flat cobalt rectangle rotated -6°, with two sparkles and a 22px opaque
ink cast shadow. It appears only above 1120px and never takes width from the
headline or the reading column. It is the same vocabulary as `.pieza`, at cover
scale.

### Motion
- **Easing:** `--curva: cubic-bezier(.4,0,.6,1)` for state and loops,
  `--entrada: cubic-bezier(.25,.1,.3,1)` for entrances, `--expo:
  cubic-bezier(.16,1,.3,1)` for the cover's line reveal and the row nudge.
- **Durations:** 160 ms micro (button colour), 240 ms fast (nav, skip link),
  320 ms normal (scroll reveal), 560 ms/640 ms for the one authored entrance per
  page. Nothing exceeds 560 ms except the 640 ms cover lines and the ambient
  sparkle/NFC loops.
- **Properties:** `transform` and `opacity` only, plus colour on hover.
- **Reveal:** `.sube` starts at `opacity 0 / translateY(20px)` and is released by
  an IntersectionObserver at threshold 0.14 with a -8% bottom margin. Stagger is
  60 ms per sibling, capped at six, counted by a `Map` keyed on the parent node —
  so each group counts its own children, and a page with many groups never
  accumulates a long delay. A 2600 ms timeout releases everything in case the
  tab opened in the background.
- **Reduced motion:** durations collapse to 0.01 ms *and* the initial states are
  forced visible (`.sube`, the cover lines, the signature, the availability chip,
  the action row, the underline). Killing duration alone would leave
  observer-driven content invisible forever.

## Do's and Don'ts

### Do:
- **Do** alternate paper and cobalt full-bleed bands, and use the inversion to
  express rank instead of growing the type.
- **Do** draw structure with 1px ink hairlines and `gap: 0`; let cells share
  edges and move the border when a grid collapses.
- **Do** cast shadows as `Xpx Xpx 0` with no blur, in `var(--tinta)` on paper
  and `rgba(0,0,0,.3)` on cobalt.
- **Do** compute the contrast ratio of any new text colour against its actual
  ground before shipping it, and record the number in a comment as the existing
  tokens do.
- **Do** make the price the largest object in its region and set figures with
  tabular numerals.
- **Do** animate `transform` and `opacity` only, on
  `cubic-bezier(.4,0,.6,1)` at 160/240/320 ms, and cap staggers at six steps of
  60 ms.
- **Do** keep every text state reachable: `:focus-visible` is a 2px flame-ground
  outline at 3px offset, switching to on-cobalt inside a plate, and hover states
  are reverted under `@media(hover: none)`.
- **Do** write every string through `t(en, es)`, format money through `euros()`
  and figures through `num()` so thousands and decimal separators switch with
  the language, and prefix assets with `A` so the Spanish build resolves `../`.
- **Do** self-host any new typeface in `fuentes/`, subset to latin and
  latin-ext, and only the weights used — the footer's "nothing from a third
  party" is a design commitment.

### Don't:
- **Don't** set functional text below 11px — a label that names a datum, a link
  affordance, a chip or a corner tag. The tracked mono label is 11px/0.2em, not
  10px/0.26em, and being on the ramp is not a defence.
- **Don't** put a pulsing status dot on the page. It reads as SaaS chrome, not
  as airbrush; the availability chip says it in words and the sparkles carry the
  ambient motion.
- **Don't** put a kicker or eyebrow above a headline. Mono labels go beside
  content or under a figure.
- **Don't** set type in `{colors.fuego}` — it is a surface colour at 3.01:1.
  Links use `{colors.fuego-texto}`, white-on-flame uses `{colors.fuego-fondo}`.
- **Don't** introduce a second warm accent, or promote the regional green/blue
  out of the artefact they depict.
- **Don't** use a blurred, spread or soft drop shadow anywhere; blur exists in
  this system only as the nav bar's backdrop-filter.
- **Don't** render chrome as a smooth blend, or add any gradient background that
  is not the hard-banded chrome (the wood tabletop in the NFC scene is a depicted
  object, not a page ground).
- **Don't** round a corner. The only radii are the 2px focus outline, the status
  dot and the slider grip.
- **Don't** draw a four-point star with straight sides; the concave sides are
  what make it airbrush.
- **Don't** use a glyph icon, icon font or raster icon — the two icons in the
  build are inline SVG paths.
- **Don't** animate anything other than transform and opacity, and don't ship an
  animation that needs more than 560 ms.
- **Don't** rely on `transition-duration: 0` alone to satisfy
  `prefers-reduced-motion`; reset the initial state too.
- **Don't** hardcode a currency string, a separator or an asset path; the site
  ships in two languages from one source.
