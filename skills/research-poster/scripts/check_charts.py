#!/usr/bin/env python3
"""check_charts.py <poster.pptx>

Static check for the one known PowerPoint chart-repair trigger: a data-label POSITION
(<c:dLblPos>) on a doughnut or pie chart. PowerPoint "repairs" such a file on open by
deleting the chart. Reads the .pptx as a zip, so it needs no PowerPoint and runs on any OS.

Exit 0: no trigger found. Exit 1: trigger found (the offending chart parts are listed).
Exit 2: the file is not a .pptx.
"""
import re
import sys
import zipfile

ROUND_TYPES = ("doughnutChart", "pieChart", "pie3DChart", "ofPieChart")


def check(path: str) -> int:
    if not zipfile.is_zipfile(path):
        print(f"Not a .pptx file: {path}")
        return 2
    with zipfile.ZipFile(path) as z:
        charts = sorted(n for n in z.namelist() if re.fullmatch(r"ppt/charts/chart\d+\.xml", n))
        slide_refs = sum(
            len(re.findall(r"<c:chart\b", z.read(n).decode("utf-8", "replace")))
            for n in z.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)
        )
        bad = []
        for name in charts:
            xml = z.read(name).decode("utf-8", "replace")
            for kind in ROUND_TYPES:
                for block in re.findall(rf"<c:{kind}>.*?</c:{kind}>", xml, flags=re.S):
                    if "<c:dLblPos" in block:
                        bad.append(f"{name} ({kind})")
    print(f"native charts in file: {len(charts)}   chart frames on slides: {slide_refs}")
    if bad:
        print("REPAIR TRIGGER: data-label position set on a doughnut/pie; PowerPoint will delete:")
        for b in bad:
            print(f"  {b}")
        print("Fix: remove data_labels.position from that chart (see references/build-and-charts.md).")
        return 1
    print("OK: no doughnut/pie data-label position (the known repair trigger).")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(check(sys.argv[1]))
