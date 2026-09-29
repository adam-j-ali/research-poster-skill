# Design rules: typography, hierarchy, padding, house style

A poster is read from a distance. The title, section headers, big stat numbers, and charts carry it;
body text is tight support. When viewed fit-to-screen the body will always look small relative to the
headers and stats. That is normal and correct; do not shrink the big elements to "balance" it.

## Poster-scale type (starting sizes on a 48x27 in / 16:9 canvas)

- Title: ~50 pt, bold. Authors ~30 pt. Affiliations ~22 pt (readable, not fine print).
- Section header bars: ~38 pt bold, white on the brand band color.
- Body: ~29 pt, justified.
- Stat tile number: ~64 pt bold; caption ~27 pt.
- Chart title ~31 pt; chart subtitle (n = ...) ~23 pt; legend ~24 pt; doughnut center number ~56 pt;
  bar labels ~30 pt; bar category labels ~25 pt; value axis ~21 pt.
- References ~22 pt; footer ~24 pt. These "fine print" items still need to be genuinely readable.

If it looks too small, the lever is fewer words + bigger type, not cramming. Concise,
scannable copy is a poster virtue; bullets are fine on a poster (unlike a manuscript).

## Hierarchy + layout

- Three columns is the default. Vertically justify each column (tops and bottoms aligned, even gaps)
  for balance. Keep inter-section gaps ~0.5-0.7 in and generous text-box margins so it breathes.
- Group the results as one bordered panel or a clean cluster; do not leave charts floating with big
  uneven gaps.
- Watch for overflow: text spilling into the next section's header, or into the footer. Give each
  block enough height; when big type is added, cut words or raise the block height.
- If the frontend-design skill is installed, use it for aesthetic direction, palette, and type pairing. Keep it clean,
  grounded, professional. Avoid neon, heavy gradients, glow, and AI-generated imagery; a clean,
  restrained look reads as credible. Match whatever style conventions the author's venue expects.

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

## Authors, affiliations, logos (a real failure mode)

The abstract's submission author block is frequently NOT final. Confirm with the author:
- The final author list, affiliation numbers, and superscripts.
- Which institutions' logos to include. A multi-institution collaboration carries every collaborating
  institution's logo (e.g. the author's home institution plus the co-authors' medical center), not
  just one. Ask; do not assume one logo.
