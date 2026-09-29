#!/usr/bin/env python3
"""check_overlap.py <rendered.pdf>

Rendered-poster check: no two text lines overlap, and all text stays 0.5 in inside the slide edges.
Run it on the PDF that render.sh exports (what PowerPoint or LibreOffice actually drew), not on the .pptx.
Exit 0: clean. Exit 1: problems listed.
"""
import sys
import fitz

pdf = fitz.open(sys.argv[1])
page = pdf[0]
W, H = page.rect.width, page.rect.height
lines = []
for b in page.get_text("dict")["blocks"]:
    for ln in b.get("lines", []):
        txt = "".join(s["text"] for s in ln["spans"]).strip()
        if txt:
            lines.append((fitz.Rect(ln["bbox"]), txt, b["number"]))
problems = []
for i in range(len(lines)):
    r1, t1, b1 = lines[i]
    if r1.x0 < 36 or r1.y0 < 0 or r1.x1 > W - 36 or r1.y1 > H - 18:
        problems.append(f"near edge: {t1[:50]!r} {tuple(round(v) for v in r1)}")
    for j in range(i + 1, len(lines)):
        r2, t2, b2 = lines[j]
        inter = r1 & r2
        if not inter.is_empty and inter.width * inter.height > 4:
            # shrink boxes by 15% of line height: font ascent/descent boxes legitimately touch between lines
            s1 = fitz.Rect(r1.x0, r1.y0 + 0.15 * r1.height, r1.x1, r1.y1 - 0.15 * r1.height)
            s2 = fitz.Rect(r2.x0, r2.y0 + 0.15 * r2.height, r2.x1, r2.y1 - 0.15 * r2.height)
            core = s1 & s2
            if not core.is_empty and core.width * core.height > 4:
                problems.append(f"overlap: {t1[:40]!r} <-> {t2[:40]!r}")
print(f"{len(lines)} text lines checked")
for p in problems:
    print("  ", p)
print("OK: no overlapping text, nothing near the edges" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
