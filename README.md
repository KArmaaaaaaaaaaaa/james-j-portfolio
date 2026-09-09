# James J Projects

Websites and Google Business Profiles for neighbourhood businesses, plus a
menu that lives on the table and a photo-to-invoice tool.

## How it is built

Six static HTML pages, no framework, no build step, and not one request to a
third party — the typefaces are served from this repository.

```bash
python3 _build.py        # English — what gets published
python3 _build.py es     # Spanish, into /es/
```

| File | What it is |
|---|---|
| `_build.py` | The generator. Content lives in `t(en, es)` calls; structure and motion are shared. |
| `_sistema.css` | The visual system: tokens, type, plates, chrome, motion. |
| `img/` | Seven images, 84 KB total. The "before" ones are the same photo darkened and blurred, not a different photo — the page says so. |
| `fuentes/` | The three typefaces, latin and latin-ext subsets, 8 files. A page pulls ~75 KB of them. All SIL OFL 1.1, which allows self-hosting. |
| `_fuentes.css` | The `@font-face` rules, inlined into every page by the generator. |
| `_estilo/` | The direction analysis and the Stitch prompt. |
| `_viejo/` | The previous generator, kept as reference. |

## The visual world

Japanese 80s airbrush over an Apple chassis. Flat cobalt fields alternating
with paper; chrome as hard-banded gradients that cut rather than blend; black
cast shadows with no blur; four-point sparkles; one warm accent, never two.
Rank is carried by colour inversion between plates, never by growing type.

Motion values are measured from apple.com's own CSS, not from memory:
`cubic-bezier(.4,0,.6,1)`, 320 ms for anything that travels, 240 for states,
160 for a tap. Nothing runs past 560 ms. Only `transform` and `opacity`.

Contrast is checked, not assumed. Body text 17.32:1, links 4.83:1, the 10px
spec labels 4.58:1, and the tone-on-tone headline 3.07:1 — which is why the
cobalt highlight is `#6493f7` and not the darker blue that looked better and
failed at 1.64:1.

## Language

English, decided 2026-09-07 ahead of a move to Hamburg. Spanish is generable
from the same source because the paying customer today is a Spanish bar owner.

## What is real and what is not

The August 2026 invoice (5,574.00 €, matching by hand to the cent) is real.
The dashboard figures are invented and the page says so. The bar is an
example and its page says so. Photos are stock in the demo; for a client they
are the client's own, because Google rejects generated photos on business
profiles and EU AI Act Article 50 has required labelling since 2 August 2026.
