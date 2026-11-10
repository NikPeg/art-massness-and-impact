#!/usr/bin/env python3
"""Build a compact reach/time figure from local tables."""

import math
from figure_i18n import cli_language
from figure_captions import caption

from build_figures import (ROOT, OUT, COLORS, SNAPSHOT_LABELS,
                           line, mark, svg_doc, table_with, text, write)


def observation(value):
    """Keep missing observations distinct from zero; reject invalid input."""
    if value == "NA":
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"Invalid observation: {value!r}")
    return result


def reach_time(lang="en"):
    rows = table_with(ROOT / "data/media_use_2026.md", "weekly_reach_percent")
    width, height = 1200, 650
    left, right, top, bottom = 85, 930, 95, 550
    values = []
    for row in rows:
        reach, minutes = (observation(row[k]) for k in ("weekly_reach_percent", "weekly_minutes"))
        if reach is None or minutes is None:
            continue
        if reach > 100:
            raise ValueError("Reach cannot exceed 100 percent")
        values.append((row, reach, minutes))
    ymax = max(500, math.ceil(max(v[2] for v in values) / 100) * 100)
    x = lambda value: left + value / 100 * (right - left)
    y = lambda value: bottom - value / ymax * (bottom - top)
    body = text(30, 36, "Reach and consumption time", size=25, weight=500)
    body += text(30, 63, "Q2 2026 · Online adults 16+ · Format proxies", size=14)
    body += text(left, 87, "Minutes / week", size=13)
    for tick in range(0, ymax + 1, 100):
        body += line(left, y(tick), right, y(tick))
        body += text(left - 15, y(tick) + 5, str(tick), "end", size=13)
    for tick in range(0, 101, 20):
        body += line(x(tick), top, x(tick), bottom, "#e6e9ed")
        body += text(x(tick), bottom + 26, str(tick), "middle", size=13)
    body += text(right, bottom + 53, "Weekly reach (%)", "end", size=14)
    # Displace labels only. Every data marker stays at its exact coordinate.
    labels = {
        "short_video": (880, 145, "start"),
        "games": (680, 135, "end"),
        "long_video": (970, 345, "start"),
        "music": (970, 405, "start"),
        "series": (650, 350, "end"),
    }
    for row, reach, minutes in values:
        category = row["category"]
        px, py = x(reach), y(minutes)
        lx, ly, anchor = labels[category]
        body += line(px, py, lx - 8 if anchor == "start" else lx + 8, ly - 5, "#aab4be")
        label = SNAPSHOT_LABELS[category][0]
        body += text(lx, ly, label, anchor, size=15, weight=500)
        body += mark(px, py, COLORS[category], title=f"{label}: {reach}% / {minutes} min/week")
    body += text(30, 630, "GWI · Details: reach-time-2026.txt", size=12)
    note = caption("scatter", lang)
    write("reach-time-2026.svg", svg_doc(width, height, "Reach and consumption time", body, note), lang)
    write("reach-time-2026.txt", note, lang, source_lang=lang)


def build(lang="en"):
    OUT.mkdir(exist_ok=True)
    reach_time(lang)


if __name__ == "__main__":
    build(cli_language())
    print("Generated reach/time SVG and adjacent TXT annotation")
