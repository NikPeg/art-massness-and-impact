#!/usr/bin/env python3
"""Render this dossier's Markdown data as standalone English SVG figures."""

from pathlib import Path
import html
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
SUBJECTIVE = ROOT / "author-interpretations"
YEARS = list(range(2021, 2026))
AXES = ["reach", "time", "frequency", "money", "recognition", "life_impact"]
AXIS_LABELS = {axis: axis.capitalize() for axis in AXES}
AXIS_LABELS["life_impact"] = "Life impact"
NAMES = {"short_video": "Short-form video", "long_video": "Long online video (proxy)", "music": "Music", "film": "Feature films",
         "series": "Series / streaming proxy", "books": "Books",
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
    directory = SUBJECTIVE if name.startswith("radar-") else OUT
    (directory / name).write_text(content, encoding="utf-8")


def annotation(filename, title, paragraphs):
    write(Path(filename).with_suffix(".txt").name,
          title + "\n\n" + "\n\n".join(paragraphs) + "\n")


def time_series(title, subtitle, series, unit, filename, footer, width=1080):
    height, left, right, top, bottom = 575, 75, 35, 150, 430
    values = [p[1] for s in series for p in s["points"] if p[1] is not None]
    maximum = math.ceil(max(values) / 40) * 40
    x = lambda year: left + 8 + (year - 2021) / 4 * (width - left - right - 16)
    y = lambda value: bottom - value / maximum * (bottom - top)
    body = text(24, 32, title, size=23, weight=500)
    body += text(24, 57, subtitle, size=12)
    legend = []
    for i, item in enumerate(series):
        latest = next((v for _, v in reversed(item["points"]) if v is not None), None)
        label = item.get("legend_name", item["name"])
        lx = 26 + i * 350
        body += line(lx, 87, lx+22, 87, item["color"], 2)
        body += text(lx+30, 91, label, size=12)
        if latest is not None:
            body += text(lx+30, 110, f"2025: {fmt(latest, 1)} min/day", size=11)
        legend.append(f'{item["color"]}: {item["name"]} | 2025: {fmt(latest, 1)}')
    for i in range(6):
        value = maximum * i / 5
        py = y(value)
        body += line(left, py, width-right, py) + text(left-12, py+4, fmt(value, 1), "end")
    body += text(left, top-14, unit, size=11)
    for year in YEARS:
        body += text(x(year), bottom+25, year, "middle")
    for item in series:
        previous = None
        for year, value in item["points"]:
            if value is None:
                previous = None
                continue
            px, py = x(year), y(value)
            if previous and year != item.get("break_year"):
                body += line(*previous, px, py, item["color"], 2)
            body += mark(px, py, item["color"])
            previous = (px, py)
    notes = [
        "Source: BLS American Time Use Survey, annual table 11A, 2021–2025.",
        "US civilian population aged 15+; all-person daily means; main activity only. Includes offline use.",
        "TV includes films, series and other content; reading is broader than books; games/computer leisure is broader than video games.",
        "Separate population and activity definitions from the international GWI snapshot; not an online-only media comparison."
    ]
    body += line(24, 478, width-24, 478)
    for i, note in enumerate(notes):
        body += text(24, 501+i*19, note, size=11)
    write(filename, svg_doc(width, height, title, body, subtitle + "; " + " ".join(notes)))
    annotation(filename, title, [subtitle, footer, "Series colors and 2025 values (" + unit + "):\n" + "\n".join(legend),
               "Missing observations are not zeros; gaps are not connected.",
               "Data and sources: ../data/annual_indicators.md; ../sources/source_register.md."])


# Labels describe the source observation, separately from the author radar names.
SNAPSHOT_LABELS = {
    "short_video": ("Short online video", "Source category; not Instagram Reels alone"),
    "long_video": ("Long online video", "Source category; duration/orientation not isolated"),
    "music": ("Music streaming", "Streaming listening only; no embedded-music union"),
    "games": ("Video games", "Reach/time: all devices; frequency: device groups"),
    "series": ("TV streaming (all content)", "Series proxy; includes films and other programmes"),
    "film": ("Feature films", "No film-only observation"),
    "books": ("Digital books", "No comparable reading observation"),
    "pictures": ("Standalone pictures", "Not isolated from mixed platform use"),
}


def snapshot(rows, key, title, unit, filename):
    observed = [row for row in rows if num(row[key]) is not None]
    width, left, right, top, step = 1100, 290, 60, 90, 57
    grid_bottom = top + (len(observed)-1)*step + 24
    height = grid_bottom + 50
    maximum, ticks, page = {
        "weekly_reach_percent": (100, [0, 25, 50, 75, 100], 38),
        "weekly_minutes": (75, [0, 15, 30, 45, 60, 75], 40),
        "days_per_week": (7, list(range(8)), 39),
    }[key]
    x = lambda value: left + value / maximum * (width-left-right)
    population = "GWI Q2 2026 · Internet users aged 16+ in covered markets · Russia excluded"
    body = text(24, 32, title, size=23, weight=500)
    tick_unit = {"weekly_reach_percent": "%", "weekly_minutes": " min/day", "days_per_week": " days/week"}[key]
    for value in ticks:
        body += line(x(value), top-18, x(value), grid_bottom)
        body += text(x(value), grid_bottom+24, str(value) + tick_unit, "middle", size=11)
    for i, row in enumerate(observed):
        cy = top + i*step
        category = row["category"]
        label = SNAPSHOT_LABELS[category][0]
        body += text(24, cy+4, label, size=13, weight=500)
        value = num(row[key])
        if key == "weekly_minutes":
            value /= 7
        extra = num(row["additional_days_per_week"]) if key == "days_per_week" else None
        for j, val in enumerate([value] + ([extra] if extra is not None else [])):
            yy = cy + (-7 if j == 0 else 12) if extra is not None else cy
            body += line(left, yy, x(val), yy, "#cbd3dc")
            marker_title = ("Mobile games" if j == 0 else "PC/console games") if extra is not None else label
            body += mark(x(val), yy, COLORS[category], j == 1, title=marker_title)
    notes = [
        f"Source: GWI via DataReportal, Digital 2027, p. {page}. Source values: data/media_use_2026.md.",
        "Music means streaming only. TV streaming is not series-only. Missing rows are not zeros.",
        "Weekly survey time / 7 gives the displayed daily mean." if key == "weekly_minutes" else
        "Frequency means average days per week, not sessions; overlapping device groups must not be added." if key == "days_per_week" else
        "Reach means reported weekly use within the surveyed online population, not a share of all people.",
        "Standalone format proxies only; embedded images, music, text and speech have no measured combined totals here."
    ]
    description = population + "; " + " ".join(notes) + "; " + "; ".join(
        f'{SNAPSHOT_LABELS[r["category"]][0]}: {r["scope"]}' for r in rows)
    write(filename, svg_doc(width, height, title, body, description))
    annotation(filename, title, [population,
        "Source-defined categories; overlapping audiences, not a complete ranking of media formats.",
        "Horizontal axis: " + unit + ".", *notes,
        "Unavailable categories are omitted, not plotted as zeros: " + ", ".join(
            SNAPSHOT_LABELS[r["category"]][0] for r in rows if num(r[key]) is None) + ".",
        *(["Games frequency: filled circle = mobile; hollow diamond = PC/console. These groups overlap."]
          if key == "days_per_week" else []),
        "Category details:\n" + "\n".join(
            f'{SNAPSHOT_LABELS[r["category"]][0]}: {SNAPSHOT_LABELS[r["category"]][1]}' for r in rows),
        "Category scopes:\n" + "\n".join(f'{SNAPSHOT_LABELS[r["category"]][0]}: {r["scope"]}' for r in rows),
        "Plotted values, rounded to two decimals (" + unit + "):\n" + "\n".join(
            f'{SNAPSHOT_LABELS[r["category"]][0]}: '
            + fmt(float(r[key]) / 7 if key == "weekly_minutes" else float(r[key]))
            + (" (mobile); " + fmt(float(r["additional_days_per_week"])) + " (PC/console)"
               if key == "days_per_week" and num(r["additional_days_per_week"]) is not None else "")
            for r in observed)])


def radar(row, anchors):
    category = row["category"]
    scores = [None if row[a] == "NA" else float(row[a]) for a in AXES]
    width, height, cx, cy, radius = 600, 510, 300, 260, 170
    pos = lambda i, value, rr=radius: (
        cx + math.cos(-math.pi/2 + i*math.tau/len(AXES))*rr*value/10,
        cy + math.sin(-math.pi/2 + i*math.tau/len(AXES))*rr*value/10)
    path = lambda vals: " ".join(("M" if i == 0 else "L") + f"{pos(i,v)[0]:.3f},{pos(i,v)[1]:.3f}" for i,v in enumerate(vals)) + "Z"
    body = text(24, 30, RADAR_NAMES[category], size=22, weight=500)
    body += text(24, 51, "Mixed scopes · not a format/component comparison", size=11)
    for ring in [2,4,6,8,10]:
        body += f'<path d="{path([ring]*len(AXES))}" fill="none" stroke="#d3d9df"/>'
    for i in range(len(AXES)):
        px, py = pos(i,10)
        body += line(cx,cy,px,py)
    # Close the profile only when all axes have explicit author scores.
    observed_path = " ".join(("M" if i == 0 else "L") + f"{pos(i,v)[0]:.3f},{pos(i,v)[1]:.3f}"
                             for i,v in enumerate(scores) if v is not None)
    if all(score is not None for score in scores):
        body += f'<path d="{path(scores)}" fill="#2463ad" fill-opacity="0.11" stroke="#2463ad" stroke-width="2"/>'
    else:
        body += f'<path d="{observed_path}" fill="none" stroke="#2463ad" stroke-width="2"/>'
    if category == "music":
        scenarios = table_with(ROOT / "author-interpretations/music_online_scenarios.md", "scenario")
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
        body += line(24, 68, 44, 68, "#2463ad", 2) + text(50, 72, "All online music", size=11)
        body += line(24, 84, 44, 84, "#b96216", 2, "6 4") + text(50, 88, "Streaming only", size=11)
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
          "Author interpretation with mixed comparison levels; not a harmonized format or component comparison. Research supporting these exact Life impact scores or their comparative ordering has not been found in the project review. " +
          "; ".join(f"{a}: {'not assessed' if v is None else str(int(v)) + '/10'}" for a,v in zip(AXES,scores))))
    annotation(name, RADAR_NAMES[category], [
        "Mixed comparison levels: earlier author profiles, not a harmonized format or component comparison. See ../research/01_scope_and_metrics.md and ../data/media_components_2026.md.",
        "2026 | Subjective author scores, 0–10; not measured effects. Research supporting exact Life impact scores or their ordering has not been found in the project review.",
        *(["Blue: direct and embedded audible online music. Orange dashed: streaming-only reference (8/6/7), informed by GWI26. Different exposure definitions, not measured uplift. See music_online_scenarios.md."] if category == "music" else []),
        "Filled circle: numeric anchor | Hollow diamond: qualitative rationale.",
        "No overall ranking. Axes and reading guide: radar-overview.txt. Scores and rationale: subjective_scores_2026.md; score_rationales.md."])
    return name


def radar_overview(radar_names):
    """Combine profiles with category names, axis labels, and scores."""
    width, height = 2400, 1020
    body = ""
    for i, name in enumerate(radar_names):
        panel = (SUBJECTIVE / name).read_text(encoding="utf-8").strip()
        # Unique accessible names for every nested SVG in the standalone sheet.
        panel = panel.replace('id="title"', f'id="panel-{i}-title"')
        panel = panel.replace('id="desc"', f'id="panel-{i}-desc"')
        panel = panel.replace('aria-labelledby="title desc"',
                              f'aria-labelledby="panel-{i}-title panel-{i}-desc"')
        panel = panel.replace('<svg ', f'<svg x="{(i % 4) * 600}" y="{(i // 4) * 510}" ', 1)
        body += panel
    write("radar-overview.svg", svg_doc(width, height, "All eight subjective radar profiles, 2026", body,
          "Eight profiles in alphabetical order by displayed English category name, left to right, then top to bottom. Identical axes and scales. Author interpretation; research supporting these exact Life impact scores or their comparative ordering has not been found in the project review."))
    write("radar-overview.txt", (ROOT / "author-interpretations/radar_overview_annotation.txt").read_text(encoding="utf-8"))


def build():
    from build_comparison_figures import build as build_comparisons
    from build_growth_figure import build as build_growth
    from build_gwi_figures import build as build_gwi

    OUT.mkdir(exist_ok=True)
    SUBJECTIVE.mkdir(exist_ok=True)
    # Remove obsolete outputs: incompatible financial scopes must not share an axis.
    for name in ("financial-landmarks.svg", "financial-landmarks.txt"):
        (OUT / name).unlink(missing_ok=True)
    time_rows=table_with(ROOT/"data/annual_indicators.md","tv_hours_day")
    time_series("US time-use aggregates, 2021–2025","US population 15+ · All-person daily means · Main activity only",[
        {"name":name,"legend_name":short_name,"color":color,"points":[(int(r["year"]),float(r[key])*60) for r in time_rows]}
        for key,name,short_name,color in [("tv_hours_day","TV: films, series and other content","Watching TV (all content)",COLORS["series"]),
                               ("reading_hours_day","Leisure reading","Leisure reading",COLORS["books"]),
                               ("games_computer_hours_day","Games and computer leisure","Playing games / leisure computer use",COLORS["games"])]] ,
        "Minutes per day","us-time-use.svg","Source: BLS ATUS, table 11A. Categories are broader than the respective media categories.")
    media=table_with(ROOT/"data/media_use_2026.md","weekly_reach_percent")
    for key,title,unit,name in [("weekly_reach_percent","Weekly reach: format proxies, 2026","Percent of surveyed online adults","reach-2026.svg"),
                                ("weekly_minutes","Daily time: format proxies, 2026","Minutes per day","time-2026.svg"),
                                ("days_per_week","Frequency: format proxies, 2026","Days per week","frequency-2026.svg")]:
        snapshot(media,key,title,unit,name)
    score_path=ROOT/"author-interpretations/subjective_scores_2026.md"
    score_rows=sorted(table_with(score_path,"recognition"),
                      key=lambda row: RADAR_NAMES[row["category"]].casefold())
    anchor_rows=next(records for header,records in tables(score_path) if header==["category","reach","time","frequency","money"])
    anchors={r["category"]:r for r in anchor_rows}
    radar_names=[radar(r,anchors[r["category"]]) for r in score_rows]
    radar_overview(radar_names)
    build_comparisons()
    build_growth()
    build_gwi()
    figures=[("Рост потребления медиа: H1 2026 (RU)", "media-growth-h1-2026.svg"),("Reach and consumption time", "reach-time-2026.svg"),
             ("US time use","us-time-use.svg"),
             ("Weekly reach","reach-2026.svg"),("Daily time","time-2026.svg"),("Frequency","frequency-2026.svg")]
    panels="".join(f'<section><h2>{html.escape(title)}</h2><img src="{name}" alt="{html.escape(title)}" loading="lazy"><a href="{Path(name).stem}.txt">Annotation (TXT)</a></section>' for title,name in figures)
    subjective_panels='<p><a href="radar-overview.svg">Open full-size radar overview</a> · <a href="radar-overview.txt">Russian annotation (TXT)</a></p>'
    subjective_panels+='<h2>Subjective 2026 radar profiles</h2><p>Earlier mixed-scope author profiles: music includes embedded soundtracks while other profiles mostly use standalone formats. These profiles do not implement either the primary-format or media-component comparison. Scores have not been recalibrated. Author interpretation. Research supporting the exact Life impact scores or their comparative ordering has not been found in the project review.</p><div class="radars">'+"".join(
        f'<section><img src="{name}" alt="{html.escape(RADAR_NAMES[r["category"]])} radar" loading="lazy"><a href="{Path(name).stem}.txt">Annotation (TXT)</a></section>'
        for name,r in zip(radar_names,score_rows))+"</div>"
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Internet-distributed media, mass reach, and life impact</title><style>
body{font:16px/1.55 system-ui,sans-serif;color:#202a34;background:white;margin:24px auto;padding:0 20px;max-width:1100px}
img{display:block;width:100%;height:auto}section{margin:24px 0}.radars{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
@media(max-width:760px){.radars{grid-template-columns:1fr}}a{color:#2463ad}</style>
<h1>Internet-distributed media, mass reach, and life impact</h1><p>Two separate comparisons: primary work formats and media components across those formats. The snapshot figures below show broad format proxies, with music streaming explicitly labeled. Component totals are unmeasured; a painting shown in a vertical video remains image contact. <a href="../data/media_components_2026.md">Component comparison and gaps</a> · <a href="../research/01_scope_and_metrics.md">Coding rules</a>.</p><p>As of 9 November 2026. Eight categories of media content distributed through the internet. Empirical observations and contextual indicators.</p>
<p>Whole-market financial series and US diaries are contextual evidence, not online-only measurements. Financial observations remain in the source tables. The compact reach/time figure has detailed sources and limitations in its adjacent TXT annotation. The US diary and international survey are separate populations. Pictures have no matched consumption or revenue values. Long online video is a broader proxy for horizontal media works; its financial series is missing. Author interpretations and radar profiles are presented separately.</p>
<p><a href="gwi/index.html">Графики GWI на русском</a> · <a href="../README.md">Research README</a> · <a href="../research/04_limitations.md">Limitations</a> · <a href="../sources/source_register.md">Sources</a> · <a href="../author-interpretations/index.html">Author interpretations and radars</a></p>'''+panels+"</html>\n"
    write("index.html",page)
    subjective_page = '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Author Interpretations</title><style>
body{font:16px/1.55 system-ui,sans-serif;color:#202a34;background:white;margin:24px auto;padding:0 20px;max-width:1100px}
img{display:block;width:100%;height:auto}.radars{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
@media(max-width:760px){.radars{grid-template-columns:1fr}}a{color:#2463ad}</style>
<h1>Author Interpretations</h1>
<p>Здесь собраны субъективные выводы автора на основе существующих данных проекта. Выбор баллов и порядок форматов отражают авторскую интерпретацию. Исследования и статистика дают основания для размышлений, но не устанавливают эти оценки от 0 до 10.</p>
<p>Радиальные диаграммы иллюстрируют авторскую модель. Они не измеряют эффекты и не доказывают превосходство одного формата над другим. Даже точка с числовой опорой остаётся авторской оценкой.</p>
<p><a href="README.md">О разделе</a> · <a href="subjective_scores_2026.md">Баллы</a> · <a href="score_rationales.md">Обоснования</a> · <a href="02_radar_profiles.md">Разбор профилей</a> · <a href="../figures/index.html">Графики наблюдаемых данных</a></p>
<section><h2>Все восемь профилей</h2><img src="radar-overview.svg" alt="Восемь субъективных радиальных диаграмм"></section>''' + subjective_panels + "</html>\n"
    (SUBJECTIVE / "index.html").write_text(subjective_page, encoding="utf-8")
    print(f"Generated {len(figures)} empirical/context SVGs, {len(radar_names)+1} subjective SVGs and two HTML galleries")


if __name__=="__main__":
    build()
