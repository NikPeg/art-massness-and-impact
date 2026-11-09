#!/usr/bin/env python3
"""Render this dossier's Markdown data as standalone English SVG figures."""

from pathlib import Path
import html
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
YEARS = list(range(2021, 2026))
AXES = ["reach", "time", "frequency", "money", "recognition", "life_impact"]
AXIS_LABELS = {axis: axis.capitalize() for axis in AXES}
AXIS_LABELS["life_impact"] = "Life impact"
NAMES = {"short_video": "Short-form video", "long_video": "Long online video (proxy)", "music": "Music", "film": "Feature films",
         "series": "Series / streaming proxy", "books": "Books / US fiction",
         "games": "Video games", "pictures": "Pictures"}
RADAR_NAMES = {**NAMES, "long_video": "Long horizontal video", "series": "Series", "books": "Books"}
COLORS = {"short_video": "#2463ad", "long_video": "#a33c31", "music": "#b96216", "film": "#93456e",
          "series": "#7057a5", "books": "#247b77", "games": "#3a824d", "pictures": "#926c24"}


def tables(path):
    """Read simple pipe tables without interpreting narrative text."""
    result, block = [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append([v.strip() for v in line.strip().strip("|").split("|")])
        elif block:
            if len(block) >= 2:
                header = block[0]
                records = []
                for cells in block[2:]:
                    if len(cells) != len(header):
                        raise ValueError(f"Malformed table in {path}: {cells}")
                    records.append(dict(zip(header, cells)))
                result.append((header, records))
            block = []
    return result


def table_with(path, column):
    matches = [records for header, records in tables(path) if column in header]
    if len(matches) != 1:
        raise ValueError(f"Expected one table with {column!r} in {path}")
    return matches[0]


def num(value):
    return None if value == "NA" else float(value)


def fmt(value, decimals=2):
    return f"{value:,.{decimals}f}".rstrip("0").rstrip(".")


def text(x, y, value, anchor="start", size=12, weight=400):
    return (f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>')


def line(x1, y1, x2, y2, stroke="#d3d9df", width=1, dash=""):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{stroke}" stroke-width="{width}" stroke-dasharray="{dash}"/>')


def mark(x, y, color, diamond=False, title=""):
    desc = f"<title>{html.escape(title)}</title>" if title else ""
    if diamond:
        return (f'<path d="M{x},{y-5}L{x+5},{y}L{x},{y+5}L{x-5},{y}Z" '
                f'fill="white" stroke="{color}" stroke-width="1.7">{desc}</path>')
    return f'<circle cx="{x}" cy="{y}" r="3.7" fill="{color}">{desc}</circle>'


def svg_doc(width, height, title, body, description=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{html.escape(title)}</title>'
            f'<desc id="desc">{html.escape(description or title)}</desc>'
            '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#202a34}</style>'
            f'<rect width="100%" height="100%" fill="white"/>{body}</svg>\n')


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


def annotation(filename, title, paragraphs):
    write(Path(filename).with_suffix(".txt").name,
          title + "\n\n" + "\n\n".join(paragraphs) + "\n")


def time_series(title, subtitle, series, unit, filename, footer, width=1080):
    height, left, right, top, bottom = 420, 70, 30, 80, 350
    values = [p[1] for s in series for p in s["points"] if p[1] is not None]
    maximum = max(values) * 1.12
    x = lambda year: left + 6 + (year - 2021) / 4 * (width - left - right - 12)
    y = lambda value: bottom - 6 - value / maximum * (bottom - top - 12)
    body = text(22, 30, title, size=21, weight=500)
    legend = []
    for s in series:
        latest = next((p[1] for p in reversed(s["points"]) if p[1] is not None), None)
        label = s["name"] + (f' | latest: {">" if s.get("reference") else ""}{fmt(latest)}' if latest is not None else " | no selected data")
        legend.append(f'{s["color"]}: {label}')
    for i in range(5):
        value = maximum * i / 4
        py = y(value)
        body += line(left, py, width-right, py) + text(left-10, py+4, fmt(value, 1), "end")
    body += text(left, top-12, unit)
    for year in YEARS:
        body += text(x(year), bottom+23, year, "middle")
    body += text(width-right, bottom+43, "Year", "end")
    for s in series:
        previous = None
        for year, value in s["points"]:
            if value is None:
                previous = None
                continue
            px, py = x(year), y(value)
            if previous and not s.get("reference") and year != s.get("break_year"):
                body += line(previous[0], previous[1], px, py, s["color"], 2,
                             "4 3" if s.get("dashed") else "")
            body += mark(px, py, s["color"], s.get("reference", False))
            previous = (px, py)
    write(filename, svg_doc(width, height, title, body))
    annotation(filename, title, [subtitle, footer, "Series colors and latest values (" + unit + "):\n" + "\n".join(legend),
               "Hollow diamond: annualized lower-bound reference point. Missing observations are not zeros; gaps are not connected.",
               "Data and sources: ../data/annual_indicators.md; ../sources/source_register.md."])


def snapshot(rows, key, title, unit, filename):
    width, left, right, top = 900, 245, 75, 70
    grid_bottom = top + (len(rows)-1)*45 + 20
    height = grid_bottom + 80
    vals = [num(r[key]) for r in rows if num(r[key]) is not None]
    if key == "days_per_week":
        vals += [num(r["additional_days_per_week"]) for r in rows if num(r["additional_days_per_week"]) is not None]
    if key == "weekly_minutes":
        vals = [v/7 for v in vals]
    maximum = max(vals) * 1.12
    x = lambda v: left + v / maximum * (width-left-right)
    body = text(24, 30, title, size=21, weight=500)
    for i in range(5):
        v = maximum * i / 4
        body += line(x(v), top-12, x(v), grid_bottom) + text(x(v), grid_bottom+22, fmt(v, 1), "middle")
    body += text(left, grid_bottom+49, unit)
    for i, row in enumerate(rows):
        cy = top + i*45
        category = row["category"]
        body += text(left-16, cy+4, NAMES[category], "end")
        v = num(row[key])
        if v is None:
            continue
        if key == "weekly_minutes":
            v /= 7
        extra = num(row["additional_days_per_week"]) if key == "days_per_week" else None
        for j, val in enumerate([v] + ([extra] if extra is not None else [])):
            yy = cy + (-8 if j == 0 else 9) if extra is not None else cy
            body += line(left, yy, x(val), yy) + mark(x(val), yy, COLORS[category], j == 1)
            label = fmt(val)
            body += text(x(val)+10, yy+4, label)
    write(filename, svg_doc(width, height, title, body))
    annotation(filename, title, [
        "GWI Q2 2026 | Online adults 16+ in covered markets | Gaps are not zeros. Russia excluded.",
        "Source: DataReportal Digital 2027, pages 38-40. Data and boundaries: ../data/media_use_2026.md.",
        "Weekly time is divided by seven to obtain daily minutes. Frequency is days per week; device groups can overlap. For games frequency, the upper circle is mobile and the lower hollow diamond is PC/console; do not add them.",
        "Blank rows have no comparable selected observation:\n" + "\n".join(NAMES[r["category"]] for r in rows if num(r[key]) is None),
        "Category scopes:\n" + "\n".join(f'{NAMES[r["category"]]}: {r["scope"]}' for r in rows)])


def radar(row, anchors):
    category = row["category"]
    scores = [None if row[a] == "NA" else float(row[a]) for a in AXES]
    width, height, cx, cy, radius = 600, 510, 300, 260, 170
    pos = lambda i, value, rr=radius: (
        cx + math.cos(-math.pi/2 + i*math.tau/len(AXES))*rr*value/10,
        cy + math.sin(-math.pi/2 + i*math.tau/len(AXES))*rr*value/10)
    path = lambda vals: " ".join(("M" if i == 0 else "L") + f"{pos(i,v)[0]:.3f},{pos(i,v)[1]:.3f}" for i,v in enumerate(vals)) + "Z"
    body = text(24, 30, RADAR_NAMES[category], size=22, weight=500)
    for ring in [2,4,6,8,10]:
        body += f'<path d="{path([ring]*len(AXES))}" fill="none" stroke="#d3d9df"/>'
    for i in range(len(AXES)):
        px, py = pos(i,10)
        body += line(cx,cy,px,py)
    # Leave the unassessed axis open: neither zero nor a fabricated score.
    observed_path = " ".join(("M" if i == 0 else "L") + f"{pos(i,v)[0]:.3f},{pos(i,v)[1]:.3f}"
                             for i,v in enumerate(scores) if v is not None)
    body += f'<path d="{observed_path}" fill="none" stroke="#2463ad" stroke-width="2"/>'
    if category == "music":
        scenarios = table_with(ROOT / "data/music_online_scenarios.md", "scenario")
        reference = next(r for r in scenarios if r["scenario"] == "streaming_reference")
        inclusive = next(r for r in scenarios if r["scenario"] == "inclusive_online")
        assert all(row[a] == inclusive[a] for a in AXES[:3])
        points = [pos(i, float(reference[a])) for i, a in enumerate(AXES[:3])]
        segment = " ".join(("M" if i == 0 else "L") + f"{x:.3f},{y:.3f}"
                           for i, (x, y) in enumerate(points))
        body += (f'<path id="music-streaming-reference" d="{segment}" fill="none" '
                 'stroke="#b96216" stroke-width="2" stroke-dasharray="6 4">'
                 '<title>Streaming-only reference: reach 8, time 6, frequency 7; author judgments</title></path>')
        for (x, y), axis in zip(points, AXES[:3]):
            body += mark(x, y, "#b96216", title=f"Streaming-only {axis}: {reference[axis]}/10")
        body += text(300, 480, "Dashed: streaming only (8 / 6 / 7)", "middle", size=12)
    for v in [2,6,10]:
        px,py=pos(0,v)
        body += text(px+6,py+4,str(v))
    for i, (axis, score) in enumerate(zip(AXES,scores)):
        angle=-math.pi/2+i*math.tau/len(AXES)
        px,py=pos(i,10,radius+28)
        cos=math.cos(angle)
        anchor="start" if cos>.25 else "end" if cos<-.25 else "middle"
        body += text(px,py,AXIS_LABELS[axis],anchor) + text(px,py+16,"Not assessed" if score is None else f"{int(score)}/10",anchor)
        if score is None:
            continue
        qx,qy=pos(i,score)
        supported=anchors.get(axis,"NA")!="NA"
        body += mark(qx,qy,"#2463ad",not supported)
    name="radar-"+category.replace("_","-")+".svg"
    write(name,svg_doc(width,height,RADAR_NAMES[category]+" radar",body,
          "; ".join(f"{a}: {'not assessed' if v is None else str(int(v)) + '/10'}" for a,v in zip(AXES,scores))))
    guide = (ROOT / "data/radar_overview_annotation.txt").read_text(encoding="utf-8")
    annotation(name, RADAR_NAMES[category], [
        "2026 subjective profile | All scores are author judgments.",
        *(["Main blue profile: direct and embedded audible online music, including short/long video, films, series and games. Hollow main markers: unmeasured union. Dashed orange segment and filled reference points: streaming-only author judgments, reach 8 / time 6 / frequency 7, informed by GWI26 (77.4%; 301 minutes/week; 3.10 days/week). Different exposure definitions, not a measured uplift or confidence interval. See ../data/music_online_scenarios.md."] if category == "music" else []),
        "Filled circle: numeric anchor | Hollow diamond: qualitative rationale.",
        "Life impact is not assessed. The profile is open and unfilled; missing is not zero. See ../data/score_rationales.md.",
        guide.split("\n\n", 2)[2]])
    return name


def radar_overview(radar_names):
    """Combine profiles with category names, axis labels, and scores."""
    width, height = 2400, 1020
    body = ""
    for i, name in enumerate(radar_names):
        panel = (OUT / name).read_text(encoding="utf-8").strip()
        # Unique accessible names for every nested SVG in the standalone sheet.
        panel = panel.replace('id="title"', f'id="panel-{i}-title"')
        panel = panel.replace('id="desc"', f'id="panel-{i}-desc"')
        panel = panel.replace('aria-labelledby="title desc"',
                              f'aria-labelledby="panel-{i}-title panel-{i}-desc"')
        panel = panel.replace('<svg ', f'<svg x="{(i % 4) * 600}" y="{(i // 4) * 510}" ', 1)
        body += panel
    write("radar-overview.svg", svg_doc(width, height, "All eight subjective radar profiles, 2026", body,
          "Eight profiles in alphabetical order by displayed English category name, left to right, then top to bottom. Identical axes and scales; Life impact is unassessed, with no marker or closed polygon."))
    write("radar-overview.txt", (ROOT / "data/radar_overview_annotation.txt").read_text(encoding="utf-8"))


def build():
    from build_participation_figures import build as build_participation
    OUT.mkdir(exist_ok=True)
    # Remove obsolete outputs: incompatible financial scopes must not share an axis.
    for name in ("financial-landmarks.svg", "financial-landmarks.txt"):
        (OUT / name).unlink(missing_ok=True)
    time_rows=table_with(ROOT/"data/annual_indicators.md","tv_hours_day")
    time_series("US time-use aggregates, 2021–2025","US population 15+ | All-person means | Main activity only",[
        {"name":name,"color":color,"points":[(int(r["year"]),float(r[key])*60) for r in time_rows]}
        for key,name,color in [("tv_hours_day","TV: films, series and other content",COLORS["series"]),
                               ("reading_hours_day","Leisure reading",COLORS["books"]),
                               ("games_computer_hours_day","Games and computer leisure",COLORS["games"])]] ,
        "Minutes per day","us-time-use.svg","Source: BLS ATUS, table 11A. Categories are broader than the respective art forms.")
    media=table_with(ROOT/"data/media_use_2026.md","weekly_reach_percent")
    for key,title,unit,name in [("weekly_reach_percent","Weekly reach, 2026","Percent of surveyed online adults","reach-2026.svg"),
                                ("weekly_minutes","Average daily time, 2026","Minutes per day","time-2026.svg"),
                                ("days_per_week","Frequency of use, 2026","Days per week","frequency-2026.svg")]:
        snapshot(media,key,title,unit,name)
    score_path=ROOT/"data/subjective_scores_2026.md"
    score_rows=sorted(table_with(score_path,"recognition"),
                      key=lambda row: RADAR_NAMES[row["category"]].casefold())
    anchor_rows=next(records for header,records in tables(score_path) if header==["category","reach","time","frequency","money"])
    anchors={r["category"]:r for r in anchor_rows}
    radar_names=[radar(r,anchors[r["category"]]) for r in score_rows]
    radar_overview(radar_names)
    figures=[("US time use","us-time-use.svg"),
             ("Weekly reach","reach-2026.svg"),("Daily time","time-2026.svg"),("Frequency","frequency-2026.svg"),
             ("All eight radar profiles","radar-overview.svg")]
    figures += build_participation()
    panels="".join(f'<section><h2>{html.escape(title)}</h2><img src="{name}" alt="{html.escape(title)}" loading="lazy"><a href="{Path(name).stem}.txt">Annotation (TXT)</a></section>' for title,name in figures)
    panels+='<p><a href="radar-overview.svg">Open full-size radar overview</a> · <a href="radar-overview.txt">Russian annotation (TXT)</a></p>'
    panels+='<h2>Subjective 2026 radar profiles</h2><div class="radars">'+"".join(
        f'<section><img src="{name}" alt="{html.escape(RADAR_NAMES[r["category"]])} radar" loading="lazy"><a href="{Path(name).stem}.txt">Annotation (TXT)</a></section>'
        for name,r in zip(radar_names,score_rows))+"</div>"
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Internet-distributed creative media, mass reach, and life impact</title><style>
body{font:16px/1.55 system-ui,sans-serif;color:#202a34;background:white;margin:24px auto;padding:0 20px;max-width:1100px}
img{display:block;width:100%;height:auto}section{margin:24px 0}.radars{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
@media(max-width:760px){.radars{grid-template-columns:1fr}}a{color:#2463ad}</style>
<h1>Internet-distributed creative media, mass reach, and life impact</h1><p>As of 9 November 2026. Eight categories of creative content distributed through the internet. Empirical landmarks and explicitly subjective profiles.</p>
<p>Whole-market financial series and US diaries are contextual evidence, not online-only measurements. Financial observations are retained only in the source tables because their market and accounting scopes differ; no common financial chart is shown. The US diary and international survey are separate populations. Pictures have no matched consumption or revenue values. All pictures radar markers are qualitative. Long online video is a broader proxy for horizontal creative works; its financial series is missing. Radar consumption and money judgments have been revised for online distribution. Music includes embedded audible contact; its dashed streaming-only reference is a different exposure definition, not a measured uplift. Radar scores are author judgments, including points with numeric anchors.</p>
<p><a href="../README.md">Research README</a> · <a href="../research/04_limitations.md">Limitations</a> · <a href="../sources/source_register.md">Sources</a> · <a href="../data/score_rationales.md">Score rationales</a></p>'''+panels+"</html>\n"
    write("index.html",page)
    print(f"Generated {len(figures)+len(radar_names)} SVG figures and figures/index.html")


if __name__=="__main__":
    build()
