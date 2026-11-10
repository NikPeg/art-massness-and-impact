#!/usr/bin/env python3
"""Validate the package's data, local references, and generated figures."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET
from markdown_links import check_local_links
from build_figures import ROOT, AXES, AXIS_LABELS, RADAR_NAMES, SUBJECTIVE, table_with, tables


def main():
    financial=table_with(ROOT/"data/annual_indicators.md","value_billion_usd")
    assert len(financial)==40, "Expected eight financial series across five years"
    lookup={(r["series"],int(r["year"])):r for r in financial}
    assert len(lookup)==40, "Duplicate series/year"
    assert lookup[("games",2021)]["value_billion_usd"]=="NA"
    assert lookup[("games",2025)]["status"]=="estimate_2026_vintage"
    assert lookup[("short_video",2025)]["status"]=="lower_bound_run_rate"
    assert float(lookup[("books",2025)]["value_billion_usd"])==7.1+5.4
    assert float(lookup[("music",2021)]["value_billion_usd"])==23.7
    assert len(table_with(ROOT/"data/annual_indicators.md","tv_hours_day"))==5
    snapshot=table_with(ROOT/"data/media_use_2026.md","weekly_reach_percent")
    assert len(snapshot)==8
    assert next(r for r in snapshot if r["category"]=="short_video")["weekly_minutes"]=="426"
    assert next(r for r in snapshot if r["category"]=="film")["weekly_reach_percent"]=="NA"
    long_video=next(r for r in snapshot if r["category"]=="long_video")
    assert [long_video[k] for k in ("weekly_reach_percent","weekly_minutes","days_per_week")]==["81.2","299","3.36"]
    assert all(lookup[("long_video",y)]["value_billion_usd"]=="NA" for y in range(2021,2026))
    # Component exposure is a separate comparison, with no measured cross-host totals.
    components=table_with(ROOT/"data/media_components_2026.md","component")
    assert {r["component"] for r in components}=={"music","images","text","speech"}
    assert all(r[k]=="NA" for r in components for k in ("reach","time","frequency"))
    # Snapshot images contain only the title and axis values; context stays in TXT.
    for name, ticks in (
        ("reach-2026", ["0%", "25%", "50%", "75%", "100%"]),
        ("time-2026", [f"{i} min/day" for i in (0, 15, 30, 45, 60, 75)]),
        ("frequency-2026", [f"{i} days/week" for i in range(8)]),
    ):
        chart = ET.parse(ROOT/"figures"/(name + ".svg")).getroot()
        visible = [el.text or "" for el in chart.iter() if el.tag.endswith("text")]
        title = chart.find("{http://www.w3.org/2000/svg}title").text
        assert visible == [title, *ticks, "Short online video", "Long online video",
                           "Music streaming", "Video games", "TV streaming (all content)"]
        note = (ROOT/"figures"/(name + ".txt")).read_text()
        assert all(label in note for label in (
            "GWI Q2 2026", "16+", "Source: GWI via DataReportal", "Horizontal axis:",
            "Digital books", "Standalone pictures", "Feature films", "Plotted values, rounded to two decimals",
            "Source category; duration/orientation not isolated"))
    us_visible = [el.text or "" for el in ET.parse(ROOT/"figures/us-time-use.svg").getroot().iter()
                  if el.tag.endswith("text")]
    assert any("Source: BLS" in label for label in us_visible)
    assert any("Includes offline use" in label for label in us_visible)
    score_rows=table_with(ROOT/"author-interpretations/subjective_scores_2026.md","recognition")
    assert len(score_rows)==8
    for row in score_rows:
        assert all(0<=float(row[a])<=10 for a in AXES)
        assert (SUBJECTIVE/("radar-"+row["category"].replace("_","-")+".svg")).is_file()
    rationales=table_with(ROOT/"author-interpretations/score_rationales.md","rationale")
    assert len(rationales)==48
    assert {(r["category"],r["axis"]) for r in rationales}=={(r["category"],a) for r in score_rows for a in AXES}
    categories={r["category"] for r in score_rows}
    assert len(categories)==8
    assert {r["category"] for r in snapshot}==categories
    assert {r["series"] for r in financial}==categories
    anchor_rows=next(rows for header,rows in tables(ROOT/"author-interpretations/subjective_scores_2026.md") if header==["category","reach","time","frequency","money"])
    assert {r["category"] for r in anchor_rows}==categories
    assert next(r for r in anchor_rows if r["category"]=="long_video")["money"]=="NA"
    picture_snapshot=next(r for r in snapshot if r["category"]=="pictures")
    assert all(picture_snapshot[k]=="NA" for k in ("weekly_reach_percent","weekly_minutes","days_per_week","additional_days_per_week"))
    assert all(lookup[("pictures",y)]["value_billion_usd"]=="NA" for y in range(2021,2026))
    picture_anchors=next(r for r in anchor_rows if r["category"]=="pictures")
    assert all(picture_anchors[a]=="NA" for a in ("reach","time","frequency","money"))
    # Combined musical exposure must not masquerade as measured streaming use.
    music_anchors=next(r for r in anchor_rows if r["category"]=="music")
    assert all(music_anchors[a]=="NA" for a in ("reach","time","frequency","money"))
    scenarios=table_with(ROOT/"author-interpretations/music_online_scenarios.md","scenario")
    inclusive=next(r for r in scenarios if r["scenario"]=="inclusive_online")
    music=next(r for r in score_rows if r["category"]=="music")
    assert all(music[a]==inclusive[a] for a in AXES[:3])
    music_svg=ET.parse(SUBJECTIVE/"radar-music.svg").getroot()
    reference=[el for el in music_svg.iter() if el.attrib.get("id")=="music-streaming-reference"]
    assert len(reference)==1 and reference[0].attrib["stroke-dasharray"]=="6 4"
    assert all(next(r for r in anchor_rows if r["category"]==cat)["money"]=="NA"
               for cat in ("music","film","series","books","games"))
    picture_svg=ET.parse(SUBJECTIVE/"radar-pictures.svg").getroot()
    assert not [el for el in picture_svg if el.tag.endswith("circle")], "Pictures data must have no numeric-anchor circles (legend excluded)"
    questions=re.findall(r"^(\d+)\.", (ROOT/"research/06_hypotheses.md").read_text(), re.M)
    answers=re.findall(r"^\| H(\d+) \|", (ROOT/"results/01_findings.md").read_text(), re.M)
    assert list(map(int,questions))==list(range(1,31))
    assert sorted(map(int,answers))==list(range(1,31))
    for name in ("reach-2026.svg","time-2026.svg","frequency-2026.svg"):
        tree=ET.parse(ROOT/"figures"/name)
        height=float(tree.getroot().attrib["height"])
        assert all(0<=float(el.attrib["y"])<height for el in tree.iter() if el.tag.endswith("text"))
    svgs=list((ROOT/"figures").glob("*.svg")) + list(SUBJECTIVE.glob("*.svg"))
    assert not list((ROOT/"figures").glob("radar-*")), "Radars belong in the author-interpretation folder"
    # Compact comparisons preserve exact point coordinates and ship detailed sidecars.
    scatter = ET.parse(ROOT/"figures/reach-time-2026.svg").getroot()
    circles = [el for el in scatter if el.tag.endswith("circle")]
    observed = [r for r in snapshot if r["weekly_reach_percent"] != "NA" and r["weekly_minutes"] != "NA"]
    assert len(circles) == len(observed) == 5
    for point, row in zip(circles, observed):
        assert abs(float(point.attrib["cx"]) - (85 + float(row["weekly_reach_percent"]) / 100 * 845)) < 1e-8
        assert abs(float(point.attrib["cy"]) - (550 - float(row["weekly_minutes"]) / 500 * 455)) < 1e-8
    for name in ("reach-time-2026",):
        assert (ROOT/"figures"/(name + ".txt")).is_file()
        assert "https://" in (ROOT/"figures"/(name + ".txt")).read_text()
        tree = ET.parse(ROOT/"figures"/(name + ".svg")).getroot()
        assert all(0 <= float(el.attrib["x"]) <= float(tree.attrib["width"])
                   and 0 <= float(el.attrib["y"]) <= float(tree.attrib["height"])
                   for el in tree.iter() if el.tag.endswith("text"))
    # GMI26 transcription and plotted percentage signs must agree.
    growth = table_with(ROOT/"data/media_growth_h1_2026.md", "change_percent")
    assert len(growth) == 12
    assert growth[0]["weekly_hhmm"] == "7:06" and growth[0]["change_percent"] == "5.2"
    assert growth[-1]["weekly_hhmm"] == "4:15" and growth[-1]["change_percent"] == "-5.9"
    chart = ET.parse(ROOT/"figures/media-growth-h1-2026.svg").getroot()
    bars = [el for el in chart.iter() if "data-category" in el.attrib]
    assert len(bars) == 12
    for bar, row in zip(bars, sorted(growth, key=lambda r: float(r["change_percent"]), reverse=True)):
        value = float(row["change_percent"])
        assert bar.attrib["data-category"] == row["category"]
        assert float(bar.attrib["data-value"]) == value
        assert abs(float(bar.attrib["width"]) - abs(value)*36) < 1e-8
        assert abs(float(bar.attrib["x"]) - min(850, 850+value*36)) < 1e-8
    assert all(0 <= float(el.attrib["x"]) <= 1120 and 0 <= float(el.attrib["y"]) <= 1030
               for el in chart.iter() if el.tag.endswith("text"))
    assert (ROOT/"sources/assets/gmi26-chart-573622.png").is_file()
    assert len(svgs)==15
    for path in svgs:
        tree=ET.parse(path)
        assert tree.getroot().tag.endswith("svg")
    overview=ET.parse(SUBJECTIVE/"radar-overview.svg").getroot()
    ns="{http://www.w3.org/2000/svg}"
    panels=overview.findall(f"{ns}svg")
    assert len(panels)==8
    for panel, row in zip(panels, sorted(score_rows, key=lambda row: RADAR_NAMES[row["category"]].casefold())):
        individual=ET.parse(SUBJECTIVE/("radar-"+row["category"].replace("_","-")+".svg")).getroot()
        assert panel.find(f"{ns}desc").text==individual.find(f"{ns}desc").text
        profile=[p for p in individual.findall(f"{ns}path") if p.attrib.get("fill-opacity")=="0.11"]
        assert len(profile)==1 and profile[0].attrib["d"].endswith("Z"), "Scored profile must be closed"
        assert profile[0].attrib["d"].count("L")==len(AXES)-1
        assert "Author interpretation" in individual.find(f"{ns}desc").text
        assert "Not assessed" not in " ".join(individual.itertext())
    ids=[el.attrib["id"] for el in overview.iter() if "id" in el.attrib]
    assert len(ids)==len(set(ids)), "Duplicate SVG accessibility IDs"
    assert not overview.findall(f".//{ns}image"), "Overview must be self-contained"
    annotation=(SUBJECTIVE/"radar-overview.txt").read_text(encoding="utf-8")
    assert annotation==(ROOT/"author-interpretations/radar_overview_annotation.txt").read_text(encoding="utf-8")
    assert all(f"{AXIS_LABELS[axis]} —" in annotation for axis in AXES)
    broken = check_local_links(ROOT)
    assert not broken, "Broken local Markdown links (file, line, target, reason):\n" + "\n".join(map(str, broken))
    for path in svgs:
        if path.name == "media-growth-h1-2026.svg":
            continue  # Explicitly Russian GMI26 reproduction.
        assert not re.search(r'[\u0400-\u04ff]', " ".join(ET.parse(path).getroot().itertext())), f"Non-English SVG text: {path}"
    assert (SUBJECTIVE/"README.md").is_file()
    assert (SUBJECTIVE/"index.html").is_file()
    print("PASS: 40 financial cells; 5 US years; 8 snapshot rows; exact comparison coordinates; 48 subjective scores and rationales; 15 SVGs; TXT annotations; local files and section anchors; English figures plus Russian growth chart.")


if __name__=="__main__":
    main()
