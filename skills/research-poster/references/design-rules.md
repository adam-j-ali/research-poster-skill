# Design rules: typography, hierarchy, padding, house style

A poster is read from a distance. The title, section headers, big stat numbers, and charts carry it;
body text is tight support. When viewed fit-to-screen the body will always look small relative to the
headers and stats. That is normal and correct; do not shrink the big elements to "balance" it.

## Readability floor (an ePoster is read on a screen)

Size type for the screen it will be shown on, not for print. On a 48 in wide 16:9 slide shown
full-screen at 1920x1080, 1 pt comes to 0.56 px:

| size | on a 1080p screen | use |
|---|---|---|
| 22 pt | 12 px | the floor: nothing smaller, anywhere, chart text included |
| 24-26 pt | 13-15 px | references, chart ticks and legends, notes |
| 28-30 pt | 16-17 px | body text |
| 34 pt | 19 px | chart titles |
| 50-60 pt | 28-34 px | the title and the main-finding sentence |

Enforce the floor with `scripts/check_fonts.py <pptx> --min 22` (it reads every size written in the
slide and chart XML) and put the same check at the end of the build, so a too-small size fails the
build. python-pptx writes an 18 pt default into every chart; set `chart.font.size` on each chart so no
unsized chart text falls back to it. Then look at the render downscaled to exactly 1920x1080 and crop
the densest regions at 1:1 (see rendering-qa.md): the numbers above say what should be legible, the
crop shows whether it is.

If it does not fit at these sizes, the lever is fewer words and fewer panels, not smaller type. A
chart that repeats information shown elsewhere is the first thing to cut. Concise, scannable copy is a
poster virtue; bullets are fine on a poster (unlike a manuscript).

## Starting sizes (48x27 in / 16:9 canvas)

- Title ~60 pt bold; authors ~30 pt; affiliations ~26 pt.
- Section headings ~38 pt bold; body ~28-30 pt.
- Stat or headline number ~46-64 pt bold; its caption ~27 pt.
- Chart title ~34 pt (phrase it as the finding: "Adoption rose every year"); chart
  subtitle ~24 pt with the n and p-values; legend and ticks ~23-24 pt; data labels ~25 pt.
- References ~24-26 pt; footer and disclosure ~23 pt.

## Hierarchy + layout

- Three columns is the default. Vertically justify each column: tops and bottoms aligned, equal gaps.
  In code, place each column's blocks with one helper that divides the leftover height into equal gaps
  and asserts a minimum gap, so an overfull column fails the build instead of overflowing.
- One element carries the poster. A strong pattern (used by several universities' own templates) is a
  dark centre panel that states the main finding as one sentence, with the key numbers in the accent
  colour and the supporting visual below it. Everything around it stays quiet.
- For a proportion of patients or eyes, a dot chart with one dot per subject (filled = success, ring =
  missed target, muted = needed further treatment) is honest, readable at a glance, and shows n
  without a label. Build the dots as native shapes so they stay editable.
- Break subtitles where you mean them to break: pass a list of lines and write each as its own
  paragraph, rather than letting a long string wrap mid-phrase.
- Watch for overflow: text spilling into the next section's header, or into the footer. Run
  `scripts/check_overlap.py` on the rendered PDF; it lists any two text lines that touch.
- If the frontend-design skill is installed, use it for aesthetic direction, palette, and type pairing.
  Keep it clean, grounded, professional. Avoid neon, heavy gradients, glow, and AI-generated imagery; a
  clean, restrained look reads as credible. Match whatever style conventions the author's venue expects.

## Contrast

Choose label colors by the background they sit on: white on dark fills, dark ink on light
(pale accent or gray) fills. Never dark-on-dark or white-on-light. For native doughnuts you cannot per-point
color labels safely, so keep labels off the slices (percentage in legend + big center number).

## House-style extraction (when a reference poster .pptx is given)

Reuse the author's existing look; do not invent one. With python-pptx:
- Slide size (many academic posters are 48x48 square print; ePosters are usually 16:9).
- Palette: read the fill colors of the header/footer bands and accent strips (solid RGB).
- Fonts and sizes per shape; the section-bar structure (colored bar + white centered header).
- Logo: it is often a vector (EMF) python-pptx/PIL cannot read. Render the reference to an image
  (`bash ${CLAUDE_SKILL_DIR}/scripts/render.sh`) and crop the logo, making its background transparent so it drops onto the
  band cleanly.
Match these tokens exactly in the new poster.

With no reference poster, use the institution's published brand kit (colour guide, typography rule,
official poster template and its logo files); `references/venues.md` covers finding and converting them.

## Authors, affiliations, logos (a real failure mode)

The abstract's submission author block is frequently NOT final. Confirm with the author:
- The final author list, affiliation numbers, and superscripts.
- Which institutions' logos to include. A multi-institution collaboration carries every collaborating
  institution's logo (e.g. the author's home institution plus the co-authors' medical center), not
  just one. Ask; do not assume one logo.
