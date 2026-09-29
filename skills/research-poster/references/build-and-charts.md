# Build approach + charts (native-editable, PowerPoint-safe)

Build the poster with **python-pptx** (>= 1.0). Everything is a native object: text boxes, rounded
rectangles for section bands and diagram boxes, stat tiles, and native charts. One editable data
block at the top of the build script drives every chart and callout, so updated numbers are a
one-line change. Assert every displayed percentage recomputes to the source number before saving.

Start from `examples/build_poster_example.py` (editable charts, the default) or
`examples/make_charts_example.py` (matplotlib images). Adapt content and house-style tokens;
do not rebuild the helpers (`rect`, `textbox`, `para`, `section_header`, `flow_column`, `stat_tile`).

## The one hard rule for native charts

PowerPoint validates chart XML on open. If it dislikes the XML it does not just warn, it
**"repairs" the file by deleting the chart** (dialog: "PowerPoint couldn't read some content ...
Repaired and removed it"). An A/B/C/D test isolated the trigger precisely:

- SAFE: per-slice fills, legend, percentage/value data labels, `number_format`,
  `number_format_is_linked = False`, axis tick-label fonts, native tables.
- BREAKS IT: **setting a doughnut/pie data-label POSITION** (e.g. `data_labels.position =
  XL_LABEL_POSITION.CENTER`). This alone makes PowerPoint repair-and-remove the chart.

So: never set `data_labels.position` on a doughnut/pie. Build charts fresh (never `replace_data` a
mismatched chart). Check with `python3 ${CLAUDE_SKILL_DIR}/scripts/check_charts.py <pptx>` before rendering.

## Doughnut recipe (editable, readable, no position setting)

Because you cannot set label position and cannot per-point-color labels reliably, do NOT put labels
on the slices. Instead:

- Put the percentage in the **legend text**: categories = `["Offers telehealth (82%)",
  "None (18%)"]`, legend at bottom, big font.
- Put the headline percentage as a **big number centered in the doughnut hole** (a separate
  textbox overlaid at the ring center, brand color, ~56pt).
- Per-slice fills via `plot.series[0].points[i].format.fill` (safe). Keep brand colors.
- `plot.has_data_labels = False`.

## Bar recipe (editable)

- `XL_CHART_TYPE.BAR_CLUSTERED`, series fill + per-point fills (safe).
- Data labels: `show_value = True`, `number_format = '0.0"%"'` (whole-number formats like `'0.#"%"'`
  render an ugly trailing dot "50.%"; `'0.0"%"'` gives clean "50.0%"). Brand-color label font.
- Category and value axis tick-label fonts set for readability. Do not set label position.
- Give the value axis headroom so the longest bar's label does not clip.

## Editable vs image charts (the tradeoff)

- Native (default): fully editable in PowerPoint (double-click to change data/colors), tiny file,
  no repair prompt. Slightly less custom (no leader lines, standard label placement).
- Images (matplotlib): pixel-perfect (leader line for a tiny slice, exact label text, luminance-based
  label contrast) but not editable. Use when the author wants the most polished static look.

The matplotlib path (image example) also carries these fixes worth reusing if you go that way:
rotate the structure doughnut (`startangle`) so labels sit at top/bottom (never clip at 3/9 o'clock);
`clip_on=False` + inward label radius; give the bar `xlim` headroom; choose label color by wedge
luminance (dark text on light fills, white on dark fills); small slice label placed OUTSIDE with
a leader line.

## Honest chart-type choice

- **Doughnut / pie**: only for true parts-of-a-whole that sum to 100% (e.g. 82% offer telehealth / 18% none).
- **Horizontal bar**: for independent or NON-mutually-exclusive proportions that share a denominator
  but overlap (e.g. barriers reported: 55.9% broadband, 44.1% reimbursement, 32.4% staff training). A pie here is
  statistically wrong.
- **Big-number tile**: for a single figure (response rate, states, a range).
- Always label the denominator (n/N) and keep any "preliminary / collection ongoing" framing.

## python-pptx chart pitfalls (each one showed up in a real render)

- **An 18 pt default is written into every chart** (`c:txPr ... sz="1800"`). Any chart text you do not
  size falls back to it. Set `chart.font.size` (and `chart.font.name`) on every chart.
- **A single-series chart prints its series name as a title** ("Success", "1-year success"). Set
  `chart.has_title = False` unless you want that title.
- **Charts can carry a white chart-area fill.** On a coloured panel that becomes a white box, and white
  labels vanish into it. Give the chart space and the plot area an explicit no-fill:

      from lxml import etree
      from pptx.oxml.ns import qn
      def transparent(chart):
          def no_fill():
              sp = etree.Element(qn("c:spPr")); etree.SubElement(sp, qn("a:noFill"))
              etree.SubElement(etree.SubElement(sp, qn("a:ln")), qn("a:noFill")); return sp
          cs = chart._chartSpace
          for old in cs.findall(qn("c:spPr")): cs.remove(old)
          cs.find(qn("c:chart")).addnext(no_fill())          # schema order: c:chart, c:spPr, c:txPr
          pa = cs.find(qn("c:chart")).find(qn("c:plotArea"))
          for old in pa.findall(qn("c:spPr")): pa.remove(old)
          ext = pa.find(qn("c:extLst"))
          (ext.addprevious if ext is not None else pa.append)(no_fill())

- **Stacked bars label their zeros.** Use `series.data_labels` with `number_format = "0;;;"` so zero
  segments print nothing, and set the label colour per series (white on the dark series, ink on the
  light one). Keep the default (centre) label position on stacked charts.
- **Line charts:** per-point labels on the first and last points (`points[i].data_label`, custom text,
  `position` ABOVE for the upper series and BELOW for the lower) rendered cleanly and triggered no
  repair; the hard rule stays specific to doughnut and pie positions. Use distinct markers (circle vs
  square) as well as colour.
- **A short chart truncates multi-line data labels** with an ellipsis. Give it height, use one-line
  labels, or drop the chart if another one already shows the same breakdown.
- Put legends at the top with `include_in_layout = False` so they do not squeeze the plot.

## One colour per group, everywhere

Give each comparison group one colour and keep it on every chart (for example group A in the brand's
primary colour, group B in its accent), so the reader learns the key once. If the accent is light (a
pale gold on white fails 3:1 contrast), relieve it with direct value labels on every mark, a dark
outline on markers and bars, and ink-coloured label text; that is the fix a palette validator asks for.
