# Rendering + self-QA

## Rendering a .pptx to an image (cross-platform)

    bash ${CLAUDE_SKILL_DIR}/scripts/render.sh "<poster.pptx>" "<out.pdf>" "<out.png>" 1.7

`render.sh` picks a renderer automatically:

1. **LibreOffice headless** (default, works on Linux / Windows / macOS): `soffice --headless
   --convert-to pdf`. This is the portable path; most environments have LibreOffice or can install it.
2. **Microsoft PowerPoint on macOS** (fallback): drives PowerPoint via AppleScript to export a PDF.
   It wraps the AppleScript in `with timeout of 280 seconds` (PowerPoint's default AppleEvent timeout
   is ~120 s and chart-heavy or large posters exceed it, giving error -1712), polls until PowerPoint
   is actually ready to be scripted (a fixed delay races the launch and gives -609 "Connection is
   invalid"), and retries up to 3 times. Because it restarts PowerPoint without saving, it refuses
   (exit 2, "POWERPOINT IS OPEN") when PowerPoint is already running: ask the user to save and quit
   it first, so their own open presentations are never lost. The first export on a machine also triggers a one-time macOS
   prompt to allow the terminal to control PowerPoint. Approve it, or the export fails silently.
   PowerPoint is sandboxed, so the first time it opens a file from a new folder it may also show a
   "Grant File Access" dialog, and the export waits until someone clicks Grant. If a render seems
   frozen, ask the user to look at PowerPoint for that dialog before retrying. The grant is per
   folder: keep every render (tests included) in one output folder PowerPoint has already been
   granted, and copy a test file there rather than rendering from a fresh temporary folder. If
   you set `PYTHON=...`, that interpreter is used for the pypdfium2 rasterize step (handy when
   pypdfium2 lives in a conda env rather than system `python3`).

Then it rasterizes the PDF to PNG with **pypdfium2** (self-contained, no poppler needed). Render the
abstract PDF directly with pypdfium2 as well.

Note: LibreOffice and PowerPoint render charts slightly differently (fonts, spacing). If you tuned a
poster against one renderer, spot-check it in the other before final delivery if the audience will
open it in PowerPoint.

## Chart-repair check (native charts, any OS)

After building native charts, check the file for the known repair trigger:

    python3 ${CLAUDE_SKILL_DIR}/scripts/check_charts.py "<poster.pptx>"

It reads the chart XML inside the .pptx (no PowerPoint needed), reports how many native charts the
file holds, and exits 1 naming each doughnut/pie that carries a data-label position (`<c:dLblPos>`),
the setting PowerPoint answers by deleting the chart on open. Remove it (see build-and-charts.md).
It checks for that known trigger only, so still look at the render: every chart you built should be
in the PNG.

## Readability and overlap checks (any OS)

    python3 ${CLAUDE_SKILL_DIR}/scripts/check_fonts.py "<poster.pptx>" --min 22
    python3 ${CLAUDE_SKILL_DIR}/scripts/check_overlap.py "<rendered.pdf>"

`check_fonts.py` reads every font size in the slide and chart XML, prints what the smallest and most
common sizes come to in pixels on a 1920 px screen, and exits 1 if anything is below the floor.
`check_overlap.py` reads the text lines out of the rendered PDF (what the renderer actually drew) and
exits 1 if any two lines overlap or any text sits within 0.5 in of the slide edge. Both were proven
against deliberately broken files; rerun that kind of probe if you change them.

Then judge legibility the way a viewer will see it: downscale the render to exactly 1920x1080 and crop
the densest regions (references, chart labels, the methods panel, light text on dark panels) at 1:1.
Look at those crops, not at the full-resolution render, which flatters small text.

    python3 -c "from PIL import Image; im=Image.open('poster.png').resize((1920,1080), Image.LANCZOS); \
      im.save('screen_1080p.png'); im.crop((0, 780, 560, 1075)).save('crop_refs.png')"

## QR codes

Encode with the `qrcode` package, or on macOS with no install: compile
`${CLAUDE_SKILL_DIR}/scripts/qr.swift` (`swiftc -O qr.swift -o qr`), which uses the system's CoreImage
to `encode` a URL to a crisp PNG and to `decode` a PNG back to text. Every code on the poster must
decode to exactly the URL it was given: assert that in the build, then crop the codes out of the
rendered PNG (and the 1080p downscale) and decode those too. Until the author supplies the real links,
encode a plain-text placeholder (not a dummy URL anyone could open), overlay a visible PLACEHOLDER tag,
and keep the output named DRAFT.

## Self-QA loop (do this to a high bar before showing the user)

Render, look at the PNG, and check every item, then fix and re-render. Iterate until clean:

- No text overflow: nothing spills into the next section's header or the footer band.
- No clipping: chart data labels and axis labels are fully visible (give bars xlim headroom; keep
  doughnut labels off the slice edges).
- Type is big enough: check_fonts.py passes at the floor, and the 1:1 crops of the 1080p view are
  comfortably readable, fine print included (references, footer, affiliations, chart captions).
- check_overlap.py passes on the rendered PDF.
- Padding is breathable: even gaps, generous margins, nothing cramped; nothing floating in a void.
- Contrast is strong everywhere (label color vs its background).
- Columns align (tops and bottoms), the layout reads as one system.
- Numbers are correct and match the source (the build already asserts this; eyeball it too).
- check_charts.py passes and every chart you built appears in the render.
- The house-style palette, fonts, and logo match the reference when one was provided.

A picture is worth a thousand tokens: always view the render, do not judge from the code.
