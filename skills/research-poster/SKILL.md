---
name: research-poster
description: >
  Turns a PDF abstract into a polished, fully-editable scientific conference poster (.pptx + PDF +
  preview) in a matched house style, with honest charts, verified citations, big readable
  typography, and a render-and-QA loop. Use whenever the user wants to make, build, design, or
  create a research poster, scientific poster, academic poster, conference poster, or ePoster
  (e.g. for RSNA, AHA, ASH, ASCO, ARVO, AAO, SNIS, or a residency research day) from an abstract,
  paper, or study; to imitate an existing poster's style with new content; or when they
  mention turning an abstract or paper into a poster, a poster from a PDF, or updating a poster's
  data, charts, layout, or making poster text bigger or cleaner. Builds native, editable PowerPoint
  charts by default (avoiding the PowerPoint chart-repair prompt), or polished image charts on request.
---

<objective>
Produce a submission-ready, on-brand scientific poster from a PDF abstract. The deliverable is an
editable PowerPoint (.pptx) plus a PDF and a preview PNG. Everything is native and editable by
default: text, section bands, stat tiles, and charts. The data, numbers, and citations are always
real and verified; the design is readable from a distance, breathable, and matched to the author's
house style (extracted from a reference poster when one is provided).

This skill encodes a workflow that was hardened in practice. Read the matching reference BEFORE the
step that needs it, not afterwards to check your work (by then the mistake is in the output); do not
reinvent the parts that are already solved (chart-safety, rendering,
typography scale). Scripts live in `${CLAUDE_SKILL_DIR}/scripts/`; worked examples and deep guidance
live in `${CLAUDE_SKILL_DIR}/references/`. Rendering uses LibreOffice (cross-platform) or Microsoft
PowerPoint on macOS; see `references/rendering-qa.md`.
</objective>

<requirements>
- python 3 with: python-pptx (>= 1.0), matplotlib, pdfplumber, pypdfium2, pillow, pypdf.
- A renderer: LibreOffice (`soffice`/`libreoffice` on PATH, any OS) OR macOS with Microsoft PowerPoint.
  The chart-repair check (`scripts/check_charts.py`) needs only python, on any OS.
- Install: `pip install python-pptx matplotlib pdfplumber pypdfium2 pillow pypdf` (add `qrcode` if
  the poster carries QR codes). If pip refuses with "externally-managed-environment", use a venv:
  `python3 -m venv ~/.venvs/poster && ~/.venvs/poster/bin/pip install <same list>`, run the build
  with that python, and pass `PYTHON=~/.venvs/poster/bin/python` to render.sh.
</requirements>

<companion_skills>
Everything this skill needs is bundled; the build, render, and check run on the scripts here alone.
These optional skills add polish. Use any that are installed. If one is missing, carry on without it
and mention the one-line install to the user once; never stop for it.

| Skill | Adds | Install (in Claude Code) |
|---|---|---|
| Anthropic `pptx` + `pdf` (`document-skills`) | editing an existing poster, hard PDFs | `/plugin marketplace add anthropics/skills`, then `/plugin install document-skills@anthropic-agent-skills` |
| `frontend-design` | palette, type pairing, layout direction | `/plugin install frontend-design@claude-plugins-official` |
| K-Dense `citation-management` (MIT) | PubMed / DOI lookup, formatted references | copy `skills/citation-management` from github.com/K-Dense-AI/scientific-agent-skills into `~/.claude/skills/` |
| K-Dense `scientific-visualization` (MIT) | journal-style matplotlib figures (image-chart route) | same repo, `skills/scientific-visualization` |

Leave out K-Dense `pptx-posters` (an HTML/CSS poster route that competes for the same requests) and
`scientific-writing` (manuscript prose that bans the bullets a poster needs). Citation checks need no
extra skill: web search and fetch against PubMed / Crossref / doi.org do the job.
</companion_skills>

<execution_context>
Run interactively OR fully autonomously. Every gate below is an `AskUserQuestion` with a clearly
marked recommended default, so an autonomous run just takes the defaults and states them.

- 🟢 Auto (no ask): read inputs, research, extract house style, build, render, self-QA and iterate,
  git-init + commit in the poster's own working dir, clean up intermediates.
- 🟡 Ask (with a recommended default): poster dimensions / venue spec, author + affiliation + logo
  confirmation, tone level, citation depth, chart engine (editable-native vs images), and whether
  the data is final.
- 🔴 Never: fabricate any number, result, or citation; alter the study's reported findings; overwrite
  a file the user has already finalized (always write a separate copy); ship a file that triggers
  PowerPoint's repair prompt.
</execution_context>

<principles>
- Reiterate the plan and confirm before building when working with a user; pair questions with a
  recommendation so the workflow can also run autonomously.
- Explore and verify, do not assume. Research with web search and a web reader; consult current
  library documentation for any API before using it. Verify every citation against PubMed or a DOI.
- Keep it lean and DRY. Reuse the bundled scripts and examples; adapt, do not rebuild. Drive every
  chart and callout from one editable data block so numbers update in one place.
- Design deliberately: strong visual hierarchy, generous padding, high contrast, readable-from-a-
  distance type. Avoid neon, heavy gradients, glow, and AI-generated imagery. Match the author's
  venue conventions.
- TDD-lite: assert every chart percentage recomputes to the source number before building.
- Self-QA to a high bar before showing the user: render, look, fix, repeat.
- Never fabricate data or citations, and never alter reported findings.
</principles>

<process>

<phase name="0_intake_and_confirm">
## Phase 0: Intake + confirm

1. Collect inputs: the abstract PDF (required); an optional reference poster (.pptx) for house
   style; optional logo files; any updated data.
2. Reiterate what you understood, then batch the gates (one or two `AskUserQuestion` calls, each
   option marked with the recommended default). Recommended defaults in brackets:
   - Dimensions / venue: verify the venue's ePoster spec first [default]; else 16:9 single slide
     (48x27 in) which matches most on-screen ePoster viewers.
   - Authors, affiliations, and logos: confirm against the author, not the abstract's submission
     block (it is often not final). Multiple institutions means multiple logos [ask which].
   - Tone: moderate scholarly polish [default]; data and findings never change.
   - Citations: 4-6 verified references with clickable DOIs/URLs [default].
   - Chart engine: editable native charts [default]; polished images on request.
   - Is the data final, or is more coming? If ongoing, build so numbers are trivial to update
     (single data block) and keep the preliminary framing.
3. Autonomous mode: take the defaults, state them, proceed.
</phase>

<phase name="1_read_inputs">
## Phase 1: Read every input fully

1. Optionally use companion skills if the environment has them (document/pptx and pdf, dataviz, frontend
   design, citation management, scientific visualization). They are enhancements;
   the workflow below is self-contained via python-pptx, matplotlib, and a renderer.
2. Read the abstract completely: text via `pdfplumber`, a visual render, and an OCR/image check so
   no figure is missed. Capture the title, authors, affiliations, every number, and the n/N for each.
3. If a reference poster is provided, extract its house style: slide size, palette (band + accent
   fills), fonts and sizes, section-bar structure, and the logo. Render it with
   `bash ${CLAUDE_SKILL_DIR}/scripts/render.sh` to see it. See `references/design-rules.md`.
4. Confirm python deps: `pip install python-pptx matplotlib pdfplumber pypdfium2 pillow pypdf`.
</phase>

<phase name="2_research">
## Phase 2: Research

1. Verify the venue's ePoster spec (dimensions, format, template).
2. Verify and fetch citations: real, PubMed/DOI-checked, with hyperlinks and access dates; include
   registry and grey-literature sources the author actually uses, not only journals. See
   `references/citations.md`. Never invent a citation.
3. Pull any background needed for the introduction. Consult current library docs when building.
</phase>

<phase name="3_design">
## Phase 3: Design

1. Set house-style tokens, a column grid, clear visual hierarchy, poster-scale typography, breathable
   padding, and strong contrast. See `references/design-rules.md`.
2. Choose chart types honestly: doughnut/pie only for parts-of-a-whole; a bar chart for independent
   or non-mutually-exclusive proportions; big-number tiles for single figures. Label every chart
   with its n/N. See `references/build-and-charts.md`.
3. Define one editable data block that drives every chart and callout.
</phase>

<phase name="4_build">
## Phase 4: Build (python-pptx, TDD-lite)

1. Adapt `references/examples/build_poster_example.py` (editable native charts) or
   `references/examples/make_charts_example.py` (matplotlib images) to the content and house style.
2. Build native editable charts with PowerPoint-safe styling ONLY. The single hard rule:
   never set a doughnut/pie data-label POSITION, that is the setting that makes PowerPoint
   repair-and-remove the chart. Per-slice fills, legends, percentage labels, number formats, and
   axis fonts are all safe. Put the doughnut percentage in the legend plus a big number in the hole.
   Full recipe in `references/build-and-charts.md`.
3. TDD-lite: assert every displayed percentage recomputes to the source number before saving.
4. Get authors, affiliations, and logos right per Phase 0.
</phase>

<phase name="5_render_and_self_qa">
## Phase 5: Render + self-QA loop

1. Render with `bash ${CLAUDE_SKILL_DIR}/scripts/render.sh <pptx> <out.pdf> <out.png> 1.7`
   (LibreOffice, or PowerPoint on macOS), then view the PNG.
2. For native charts, run `python3 ${CLAUDE_SKILL_DIR}/scripts/check_charts.py <pptx>`: it fails if any doughnut/pie
   carries a data-label position, the setting that makes PowerPoint delete the chart on open.
3. Fix against the `references/rendering-qa.md` checklist: no overflow or clipping, big enough type,
   breathable padding, high contrast, aligned columns, correct numbers. Iterate until it is genuinely
   good before showing the user.
</phase>

<phase name="6_deliver_git_cleanup">
## Phase 6: Deliver + git + cleanup

1. Write a SEPARATE, clearly named copy; never overwrite a file the user has finalized.
2. Deliver the .pptx, a submission PDF, and a preview PNG.
3. git-init the poster's working dir if needed and commit with a clear message (baseline first when
   iterating on an existing poster, so the prior version is preserved).
4. Remove intermediate renders and temp files; keep the reproducible build scripts.
</phase>

</process>

<success_criteria>
- [ ] Deliverable is an editable .pptx plus a matching PDF (verified page size) and preview PNG
- [ ] Charts are native and editable (default) and survive PowerPoint open with no repair prompt
- [ ] Every percentage recomputes to the source number; n/N shown; preliminary framing kept if ongoing
- [ ] Citations are all real and verified, with DOI/URL hyperlinks
- [ ] Authors, affiliations, and logos confirmed with the user
- [ ] Type is readable from a distance, padding is breathable, contrast is strong, columns align
- [ ] House style matches the reference poster when one was provided
- [ ] A separate copy was written; the user's finalized files were not touched; work is git-tracked
</success_criteria>

<error_handling>
- render.sh prints "RENDER FAILED" if no renderer is found: say so plainly and offer the two fixes
  (install LibreOffice, or use macOS with Microsoft PowerPoint). Do not surface raw AppleScript
  errors (-600 / -609 / -1712) to the user. The PowerPoint path already retries on a launch race.
- A PowerPoint render seems frozen: PowerPoint is usually waiting on a one-time macOS dialog (allow
  the terminal to control PowerPoint, or PowerPoint's "Grant File Access"). Ask the user to look at
  PowerPoint and approve it, then continue; do not kill and retry blind.
- render.sh exits 2 with "POWERPOINT IS OPEN": the PowerPoint path restarts
  PowerPoint without saving, so it refuses while the user has it open. Ask them to save and quit
  PowerPoint, then re-run. Never quit or kill PowerPoint yourself while their files are open.
- check_charts.py reports a REPAIR TRIGGER, or a native chart is missing from the render: a
  doughnut/pie data-label position was set somewhere; remove it (see references/build-and-charts.md).
- python dep missing: `pip install python-pptx matplotlib pdfplumber pypdfium2 pillow pypdf`.
</error_handling>

<references>
Read on demand, one level deep from here:
- `references/build-and-charts.md` : python-pptx build approach, the native-editable-chart safe recipe
  and the exact repair trigger to avoid, honest chart-type choices, and chart styling.
- `references/design-rules.md` : poster-scale typography and hierarchy, padding, contrast, house-style
  extraction from a reference .pptx, logos, and confirming the author block.
- `references/rendering-qa.md` : the cross-platform render path, robustness, the chart-repair check,
  and the self-QA checklist.
- `references/citations.md` : verifying, formatting (AMA/Vancouver), hyperlinking, and sourcing.
- `references/examples/` : two worked build scripts (native charts, image charts) to adapt.
</references>
