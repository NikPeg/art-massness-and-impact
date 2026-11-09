#!/usr/bin/env python3
"""Build a compact reach/time figure from local tables."""

import math

from build_figures import (ROOT, OUT, COLORS, SNAPSHOT_LABELS, annotation, fmt,
                           line, mark, svg_doc, table_with, text, write)


def observation(value):
    """Keep missing observations distinct from zero; reject invalid input."""
    if value == "NA":
        return None
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"Invalid observation: {value!r}")
    return result


def source_notes(ids):
    lines = (ROOT / "sources/source_register.md").read_text(encoding="utf-8").splitlines()
    return "Source register entries:\n" + "\n".join(
        row for row in lines if any(row.startswith(f"| {sid} |") for sid in ids))


def reach_time():
    rows = table_with(ROOT / "data/media_use_2026.md", "weekly_reach_percent")
    width, height = 1200, 650
    left, right, top, bottom = 85, 930, 95, 550
    values, missing = [], []
    for row in rows:
        reach, minutes = (observation(row[k]) for k in ("weekly_reach_percent", "weekly_minutes"))
        if reach is None or minutes is None:
            missing.append(row)
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
    records = []
    for row, reach, minutes in values:
        category = row["category"]
        px, py = x(reach), y(minutes)
        lx, ly, anchor = labels[category]
        body += line(px, py, lx - 8 if anchor == "start" else lx + 8, ly - 5, "#aab4be")
        label = SNAPSHOT_LABELS[category][0]
        body += text(lx, ly, label, anchor, size=15, weight=500)
        body += mark(px, py, COLORS[category], title=f"{label}: {reach}% / {minutes} min/week")
        records.append(f"{label}: {fmt(reach)}% weekly reach; {fmt(minutes)} minutes/week. {row['scope']}")
    body += text(30, 630, "GWI · Details: reach-time-2026.txt", size=12)
    notes = [
        "Source: GWI Q2 2026, reproduced in DataReportal Digital 2027, pages 38 and 40. "
        "Internet users aged 16+ in covered markets; Russia excluded. Not a census of all humans.",
        "Axes: reported weekly reach (%) and reported weekly minutes, as transcribed in "
        "../data/media_use_2026.md. No division by reach, multiplication by audience, or time conversion. "
        "Data points are not jittered; leader lines connect displaced labels to exact points.",
        "Observations:\n" + "\n".join(records),
        "Omitted because one or both coordinates are unavailable:\n" + "\n".join(
            f"{SNAPSHOT_LABELS[r['category']][0]}: {r['scope']}" for r in missing),
        "Missing observations are not zeros. Music is streaming-only. TV streaming includes films "
        "and other programmes and does not isolate series. Source short/long video categories do not "
        "isolate vertical/horizontal orientation. Audiences overlap; embedded components are not added.",
        "The selected point estimates put short video first in reach and games first in time. "
        "The 433 versus 426 minute contrast has not been tested for statistical significance. "
        "No complete eight-format ranking, causal effect, or life-impact estimate follows.",
        source_notes({"GWI26"}),
    ]
    write("reach-time-2026.svg", svg_doc(width, height, "Reach and consumption time", body, "\n\n".join(notes)))
    annotation("reach-time-2026.svg", "Reach and consumption time", notes)


def build():
    OUT.mkdir(exist_ok=True)
    reach_time()


if __name__ == "__main__":
    build()
    print("Generated reach/time SVG and adjacent TXT annotation")
