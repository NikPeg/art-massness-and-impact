#!/usr/bin/env python3
"""Validate the package's data, local references, and generated figures."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET
from build_figures import ROOT, AXES, AXIS_LABELS, RADAR_NAMES, table_with, tables


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
    score_rows=table_with(ROOT/"data/subjective_scores_2026.md","recognition")
    assert len(score_rows)==8
    for row in score_rows:
        assert all(0<=float(row[a])<=10 for a in AXES)
        assert (ROOT/"figures"/("radar-"+row["category"].replace("_","-")+".svg")).is_file()
    rationales=table_with(ROOT/"data/score_rationales.md","rationale")
    assert len(rationales)==48
    assert {(r["category"],r["axis"]) for r in rationales}=={(r["category"],a) for r in score_rows for a in AXES}
    categories={r["category"] for r in score_rows}
    assert len(categories)==8
    assert {r["category"] for r in snapshot}==categories
    assert {r["series"] for r in financial}==categories
    anchor_rows=next(rows for header,rows in tables(ROOT/"data/subjective_scores_2026.md") if header==["category","reach","time","frequency","money"])
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
    scenarios=table_with(ROOT/"data/music_online_scenarios.md","scenario")
    inclusive=next(r for r in scenarios if r["scenario"]=="inclusive_online")
    music=next(r for r in score_rows if r["category"]=="music")
    assert all(music[a]==inclusive[a] for a in AXES[:3])
    music_svg=ET.parse(ROOT/"figures/radar-music.svg").getroot()
    reference=[el for el in music_svg.iter() if el.attrib.get("id")=="music-streaming-reference"]
    assert len(reference)==1 and reference[0].attrib["stroke-dasharray"]=="6 4"
    assert all(next(r for r in anchor_rows if r["category"]==cat)["money"]=="NA"
               for cat in ("music","film","series","books","games"))
    picture_svg=ET.parse(ROOT/"figures/radar-pictures.svg").getroot()
    assert not [el for el in picture_svg.iter() if el.tag.endswith("circle")], "Pictures must have no numeric-anchor circles"
    questions=re.findall(r"^(\d+)\.", (ROOT/"research/06_hypotheses.md").read_text(), re.M)
    answers=re.findall(r"^\| H(\d+) \|", (ROOT/"results/01_findings.md").read_text(), re.M)
    assert list(map(int,questions))==list(range(1,28))
    assert sorted(map(int,answers))==list(range(1,28))
    for name in ("reach-2026.svg","time-2026.svg","frequency-2026.svg"):
        tree=ET.parse(ROOT/"figures"/name)
        height=float(tree.getroot().attrib["height"])
        assert all(0<=float(el.attrib["y"])<height for el in tree.iter() if el.tag.endswith("text"))
    svgs=list((ROOT/"figures").glob("*.svg"))
    assert len(svgs)==15
    for path in svgs:
        tree=ET.parse(path)
        assert tree.getroot().tag.endswith("svg")
    overview=ET.parse(ROOT/"figures/radar-overview.svg").getroot()
    ns="{http://www.w3.org/2000/svg}"
    panels=overview.findall(f"{ns}svg")
    assert len(panels)==8
    for panel, row in zip(panels, sorted(score_rows, key=lambda row: RADAR_NAMES[row["category"]].casefold())):
        individual=ET.parse(ROOT/"figures"/("radar-"+row["category"].replace("_","-")+".svg")).getroot()
        assert panel.find(f"{ns}desc").text==individual.find(f"{ns}desc").text
        profile=[p for p in individual.findall(f"{ns}path") if p.attrib.get("fill-opacity")=="0.11"]
        assert len(profile)==1 and profile[0].attrib["d"].endswith("Z"), "Scored profile must be closed"
        assert profile[0].attrib["d"].count("L")==len(AXES)-1
        assert "Author interpretation" in individual.find(f"{ns}desc").text
        assert "Not assessed" not in " ".join(individual.itertext())
    ids=[el.attrib["id"] for el in overview.iter() if "id" in el.attrib]
    assert len(ids)==len(set(ids)), "Duplicate SVG accessibility IDs"
    assert not overview.findall(f".//{ns}image"), "Overview must be self-contained"
    annotation=(ROOT/"figures/radar-overview.txt").read_text(encoding="utf-8")
    assert annotation==(ROOT/"data/radar_overview_annotation.txt").read_text(encoding="utf-8")
    assert all(f"{AXIS_LABELS[axis]} —" in annotation for axis in AXES)
    broken=[]
    for path in ROOT.rglob("*.md"):
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)',path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            if not (path.parent/target.split("#")[0]).resolve().exists():
                broken.append((str(path.relative_to(ROOT)),target))
    assert not broken, f"Broken local Markdown references: {broken}"
    text_files=[p for p in ROOT.rglob("*") if p.suffix in {".md",".py",".html",".svg"}]
    for path in text_files:
        assert not re.search(r'[\u0400-\u04ff]',path.read_text(encoding="utf-8")),f"Non-English Cyrillic text: {path}"
    from validate_participation_figures import validate as validate_participation
    validate_participation()
    print("PASS: 40 financial cells; 5 US years; 8 snapshot rows; 48 subjective scores and rationales; 15 SVGs including participation; Russian TXT; local links; English figures.")


if __name__=="__main__":
    main()
