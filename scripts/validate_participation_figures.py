#!/usr/bin/env python3
"""Check survey figure values, percentage scales, bounds, and TXT sidecars."""

import re
import xml.etree.ElementTree as ET
from build_figures import OUT
from build_participation_figures import FIGURES, observations


def validate():
    expected_values = [
        [float(r["participation_percent"]) for r in observations("activity")],
        [float(r["participation_percent"]) for r in observations("group")
         if r["group"].startswith(("Most deprived", "Least deprived"))],
    ]
    ns = "{http://www.w3.org/2000/svg}"
    for (_, filename), values in zip(FIGURES, expected_values):
        path = OUT / filename
        root = ET.parse(path).getroot()
        width, height = float(root.attrib["width"]), float(root.attrib["height"])
        labels = [el.text or "" for el in root.findall(f"{ns}text")]
        plotted = [float(label[:-1]) for label in labels if re.fullmatch(r"\d+(?:\.\d+)?%", label)]
        assert sorted(plotted) == sorted(values), f"Displayed percentages differ from source: {filename}"
        assert all(str(v) in labels for v in range(0, 101, 20)), f"Expected 0-100% scale: {filename}"
        for el in root.findall(f"{ns}text"):
            assert 0 <= float(el.attrib["x"]) < width and 0 <= float(el.attrib["y"]) < height
        sidecar = path.with_suffix(".txt").read_text(encoding="utf-8")
        assert all(term in sidecar for term in ("Source:", "https://", "Data:", "2025"))
        assert root.find(f"{ns}desc").text
    print("PASS: 2 participation figures; source percentages; 0-100% scales; label bounds; TXT annotations")


if __name__ == "__main__":
    validate()
