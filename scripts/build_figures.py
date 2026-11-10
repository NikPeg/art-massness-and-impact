#!/usr/bin/env python3
"""Render local Markdown data as English (default) or Russian SVG figures."""

from pathlib import Path
import html
import math
import xml.etree.ElementTree as ET
from figure_i18n import cli_language, localized_path, save, translate
from figure_captions import caption

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
SUBJECTIVE = ROOT / "author-interpretations"
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


def write(name, content, lang="en", source_lang="en"):
    directory = SUBJECTIVE if name.startswith("radar-") else OUT
    save(directory / name, content, lang, source_lang)


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


def snapshot(rows, key, title, unit, filename, lang="en"):
    observed = [row for row in rows if num(row[key]) is not None]
    width, left, right, top, step = 1100, 290, 60, 90, 57
    grid_bottom = top + (len(observed)-1)*step + 24
    height = grid_bottom + (75 if key == "days_per_week" else 50)
    maximum, ticks = {
        "weekly_reach_percent": (100, [0, 25, 50, 75, 100]),
        "weekly_minutes": (75, [0, 15, 30, 45, 60, 75]),
        "days_per_week": (7, list(range(8))),
    }[key]
    x = lambda value: left + value / maximum * (width-left-right)
    body = text(24, 32, title, size=23, weight=500)
    tick_unit = {"weekly_reach_percent": "%", "weekly_minutes": " min/day", "days_per_week": ""}[key]
    for value in ticks:
        body += line(x(value), top-18, x(value), grid_bottom)
        body += text(x(value), grid_bottom+24, str(value) + tick_unit, "middle", size=11)
    if key == "days_per_week":
        body += text((left + width - right)/2, grid_bottom+52, unit, "middle", size=12)
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
            if key == "days_per_week":
                body += text(x(val)+11, yy+4, fmt(val), size=12)
    kind = {"weekly_reach_percent": "reach", "weekly_minutes": "time", "days_per_week": "frequency"}[key]
    note = caption(kind, lang)
    write(filename, svg_doc(width, height, title, body, note), lang)
    write(Path(filename).with_suffix(".txt").name, note, lang, source_lang=lang)


def radar(row, anchors, lang="en"):
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
          "; ".join(f"{AXIS_LABELS[a]}: {'Not assessed' if v is None else str(int(v)) + '/10'}" for a,v in zip(AXES,scores))), lang)
    write(Path(name).with_suffix(".txt").name, caption(Path(name).stem, lang), lang, source_lang=lang)
    return name


def radar_overview(radar_names, lang="en"):
    """Combine profiles with category names, axis labels, and scores."""
    width, height = 2400, 1020
    body = ""
    for i, name in enumerate(radar_names):
        panel = localized_path(SUBJECTIVE / name, lang).read_text(encoding="utf-8").strip()
        # Unique accessible names for every nested SVG in the standalone sheet.
        panel = panel.replace('id="title"', f'id="panel-{i}-title"')
        panel = panel.replace('id="desc"', f'id="panel-{i}-desc"')
        panel = panel.replace('aria-labelledby="title desc"',
                              f'aria-labelledby="panel-{i}-title panel-{i}-desc"')
        panel = panel.replace('<svg ', f'<svg x="{(i % 4) * 600}" y="{(i // 4) * 510}" ', 1)
        body += panel
    write("radar-overview.svg", svg_doc(width, height, "All eight subjective radar profiles, 2026", body,
          "Eight profiles in alphabetical order by displayed English category name, left to right, then top to bottom. Identical axes and scales. Author interpretation; research supporting these exact Life impact scores or their comparative ordering has not been found in the project review."), lang)
    guide_name = "radar_overview_annotation.txt" if lang == "ru" else "radar_overview_annotation-en.txt"
    write("radar-overview.txt", (SUBJECTIVE / guide_name).read_text(encoding="utf-8"), lang, source_lang=lang)


def build(lang="en"):
    from build_comparison_figures import build as build_comparisons
    from build_growth_figure import build as build_growth
    from build_gwi_figures import build as build_gwi

    OUT.mkdir(exist_ok=True)
    SUBJECTIVE.mkdir(exist_ok=True)
    # Remove retired charts so rebuilds cannot reintroduce them into the gallery.
    for name in ("financial-landmarks.svg", "financial-landmarks.txt", "us-time-use.svg", "us-time-use.txt"):
        (OUT / name).unlink(missing_ok=True)
    media=table_with(ROOT/"data/media_use_2026.md","weekly_reach_percent")
    for key,title,unit,name in [("weekly_reach_percent","Weekly reach: format proxies, 2026","Percent of surveyed online adults","reach-2026.svg"),
                                ("weekly_minutes","Daily time: format proxies, 2026","Minutes per day","time-2026.svg"),
                                ("days_per_week","Frequency: format proxies, 2026","Days per week","frequency-2026.svg")]:
        snapshot(media,key,title,unit,name,lang)
    score_path=ROOT/"author-interpretations/subjective_scores_2026.md"
    score_rows=sorted(table_with(score_path,"recognition"),
                      key=lambda row: translate(RADAR_NAMES[row["category"]], lang).casefold())
    anchor_rows=next(records for header,records in tables(score_path) if header==["category","reach","time","frequency","money"])
    anchors={r["category"]:r for r in anchor_rows}
    radar_names=[radar(r,anchors[r["category"]],lang) for r in score_rows]
    radar_overview(radar_names,lang)
    build_comparisons(lang)
    build_growth(lang)
    build_gwi(lang)
    # Discover every chart, including nested galleries, after all generators finish.
    figures = []
    for path in sorted(OUT.rglob("*.svg")):
        if path.stem.endswith("-ru") != (lang == "ru"):
            continue
        chart_title = ET.parse(path).getroot().find("{http://www.w3.org/2000/svg}title")
        title = chart_title.text if chart_title is not None else path.stem
        figures.append((title, path.relative_to(OUT).as_posix()))
    panels = "".join(
        f'<section><h2>{html.escape(title)}</h2><img src="{html.escape(name)}" '
        f'alt="{html.escape(title)}" loading="lazy"><a href="{html.escape(Path(name).with_suffix(".txt").as_posix())}">'
        'Annotation (TXT)</a></section>' for title, name in figures)
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
<p>Financial observations remain in the source tables without a common-axis chart. The compact reach/time figure has detailed sources and limitations in its adjacent TXT annotation. Pictures have no matched consumption or revenue values. Long online video is a broader proxy for horizontal media works; its financial series is missing. Author interpretations and radar profiles are presented separately.</p>
<p><a href="gwi/index.html">GWI charts</a> · <a href="../README.md">Research README</a> · <a href="../research/04_limitations.md">Limitations</a> · <a href="../sources/source_register.md">Sources</a> · <a href="../author-interpretations/index.html">Author interpretations and radars</a></p>'''+panels+"</html>\n"
    write("index.html",page,lang)
    subjective_page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Author Interpretations</title><style>
body{font:16px/1.55 system-ui,sans-serif;color:#202a34;background:white;margin:24px auto;padding:0 20px;max-width:1100px}
img{display:block;width:100%;height:auto}.radars{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
@media(max-width:760px){.radars{grid-template-columns:1fr}}a{color:#2463ad}</style>
<h1>Author Interpretations</h1>
<p>Author scores reflect the author's interpretation of the project's existing data. The choice of scores and ordering of formats is subjective. Research and statistics inform the discussion but do not establish these 0–10 ratings.</p>
<p>Radar diagrams illustrate the author's model. They do not measure effects or establish the superiority of a format. Even a point with a numeric source anchor remains a subjective rating.</p>
<p><a href="README.md">About this section</a> · <a href="subjective_scores_2026.md">Scores</a> · <a href="score_rationales.md">Score rationales</a> · <a href="02_radar_profiles.md">Profile discussion</a> · <a href="../figures/index.html">Observed-data charts</a></p>
<section><h2>All eight profiles</h2><img src="radar-overview.svg" alt="Eight subjective radar profiles"></section>''' + subjective_panels + "</html>\n"
    save(SUBJECTIVE / "index.html", subjective_page, lang)
    print(f"Generated {len(figures)} empirical/context SVGs, {len(radar_names)+1} subjective SVGs and two HTML galleries")


if __name__=="__main__":
    build(cli_language())
