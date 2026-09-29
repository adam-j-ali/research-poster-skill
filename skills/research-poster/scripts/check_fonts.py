#!/usr/bin/env python3
"""check_fonts.py <poster.pptx> [--min 22] [--screen 1920]

Readability gate: reads every font size written anywhere in the slides and charts of a .pptx and
fails if any is below the floor. Also prints what the smallest and body sizes come to in pixels on a
screen of the given width, because an ePoster is read on a monitor, not on paper.

Exit 0: every size is at or above the floor. Exit 1: sizes below the floor (listed). Exit 2: not a .pptx.
"""
import argparse
import re
import sys
import zipfile
from collections import Counter

EMU_PER_INCH = 914400


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--min", type=float, default=22.0, help="smallest allowed size in points (default 22)")
    ap.add_argument("--screen", type=int, default=1920, help="screen width in pixels (default 1920)")
    a = ap.parse_args()
    if not zipfile.is_zipfile(a.pptx):
        print(f"Not a .pptx file: {a.pptx}")
        return 2
    with zipfile.ZipFile(a.pptx) as z:
        pres = z.read("ppt/presentation.xml").decode("utf-8", "replace")
        width_in = int(re.search(r'<p:sldSz[^>]*\bcx="(\d+)"', pres).group(1)) / EMU_PER_INCH
        sizes = Counter()
        for part in z.namelist():
            if re.fullmatch(r"ppt/(slides/slide\d+|charts/chart\d+)\.xml", part):
                for v in re.findall(r'\bsz="(\d+)"', z.read(part).decode("utf-8", "replace")):
                    sizes[int(v) / 100] += 1
    if not sizes:
        print("No explicit font sizes found; text inherits theme defaults, which are sized for small slides.")
        return 1
    px_per_pt = a.screen / (width_in * 72)
    small = sorted(s for s in sizes if s < a.min)
    common = sizes.most_common(1)[0][0]
    print(f"slide width {width_in:g} in; on a {a.screen}px-wide screen 1 pt = {px_per_pt:.2f} px")
    print(f"sizes {min(sizes):g}-{max(sizes):g} pt; smallest = {min(sizes) * px_per_pt:.1f} px, "
          f"most common ({common:g} pt) = {common * px_per_pt:.1f} px")
    if small:
        print(f"TOO SMALL (below {a.min:g} pt): {small}")
        return 1
    print(f"OK: nothing below {a.min:g} pt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
