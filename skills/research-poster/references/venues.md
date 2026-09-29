# Venue specs: find them at the source, and date them

A venue's rules decide the canvas, the file type, what media works, and a required disclosure. They
change every year, so verify them on the society's own pages for the current meeting and write down the
date you read them. The acceptance email and the poster-upload site usually carry the exact template;
ask the author for them first.

## How to find a venue's spec

1. The society's "presenter" or "poster" pages for this year's meeting (the abstract page is not enough).
2. The formatting page for talks: screen aspect ratio and allowed fonts usually apply to ePosters too.
3. The upload vendor the society names (for example an ePoster platform); its instructions may be public
   for other meetings that use it, which shows the platform's limits but not this meeting's deadlines.
4. The disclosure policy page: many societies require a financial disclosure on the first content slide,
   with exact wording when there is nothing to disclose.

**Check which organisation a search result is about.** Acronyms collide (AAO is ophthalmology, AAOS is
orthopaedic surgery; both used the same ePoster vendor in 2026). A search summary once attributed the
orthopaedic meeting's February deadline to the ophthalmology meeting. Open the document and read its header.

## ePoster platform limits seen in practice

- Hyperlinks, animations and embedded video usually do not survive the ePoster viewer. Put a QR code on
  the poster instead, and upload any narration through the platform's own tools.
- Screens are 16:9 (1920x1080 or 1280x720). A 16:9 canvas fills them; a 3:2 or 4:3 print template will
  show with bars at the sides.
- Standard Office fonts only, or embed the font. Arial is the safe choice.

## American Academy of Ophthalmology (AAO) 2026, verified 2026-09-29 on aao.org

- Meeting: New Orleans, October 9-12, 2026.
- Poster types: Podium Poster (6-minute moderated talk, the poster file shown on a large monitor), Poster
  Discussion (panel of 5 posters, 30 minutes), On-Demand Poster (online only; presenters need not attend).
- Upload: through the Digital Acumen APPRISOR system, "typically 4 weeks in advance" of the meeting
  (on-demand: "typically 2 weeks prior"). The acceptance email has the real date.
- Screens: "All screens will be 16:9 widescreen format, not 4:3"; 1280x720 or 1920x1080. Fonts: Office
  fonts only unless embedded. Images: resize so the larger side is at most 2000 px.
- Disclosure: financial relationships must appear "on the first content slide of their ... poster",
  "even if the presenter has no financial interest". With nothing to disclose, the required sentence is
  "I have no financial interests or relationships to disclose."
- Sources: aao.org/annual-meeting/presenter/paper-frequently-asked-questions,
  /presenter/presentation-format, /presenter/presentation-tips-disclosure,
  /named-lectures/presenter-central_papers--posters-instructions.

## Institution branding without a reference poster

University brand portals often publish their research-poster templates, logos, colour guides and
typography guides as public downloads. Use those, not a logo found by image search:

- Take the palette from the official colour guide (HEX values) and the typeface rule for PowerPoint.
- Pull the logo out of the official poster template (`ppt/media/`). Print-grade logos may be CMYK TIFFs
  that Pillow cannot open; on macOS `sips -s format png in.tif --out out.png` converts them. Crop the
  transparent margin, keep the larger side at most 2000 px, and sample the pixels to confirm the colour.
- A department-specific lockup usually has to be requested from the brand office; the parent
  institution's logo is the safe default meanwhile.
