# Reproduction scripts

Empirical inputs are Markdown tables under `../data/`. Author scores, rationales, music scenarios and the editable radar annotation are under `../author-interpretations/`.

- `build_figures.py`: reads those tables, converts selected units, and writes empirical/context SVGs and `figures/index.html`, plus radar SVGs and a separate `author-interpretations/index.html` gallery.
- `build_comparison_figures.py`: builds the compact `reach-time-2026.svg` and its TXT annotation. Can run independently; also called by the full build. Reads the Markdown inputs directly, keeps scatter coordinates exact and skips missing pairs.
- Each SVG has a matching TXT annotation generated alongside it. The three snapshot images show only titles and axis values with units; all measurement context and point values are in their TXT files. The compact reach/time figure puts full sources, definitions, omissions and caveats in TXT; the image retains only essential labels, axes, units and an annotation reference. Radars visibly identify author scores.
- `validate.py`: checks selected values, missing observations, score bounds, eight radar outputs and their combined overview, SVG syntax, and both files and section anchors in local Markdown links.

Run both with Python 3.9+. No pip packages, browser libraries, external chart CDN, network requests, or credentials are used.

The common financial chart has been removed: market totals, company revenue, cinema gross, and an annualized revenue pace cannot support a shared commercial-scale comparison. Financial observations remain in the source tables. The build still removes the obsolete common-axis financial SVG and TXT outputs. The US time-use chart and its renderer have been removed; full builds delete obsolete chart outputs. The main figures gallery discovers every SVG recursively and links each matching TXT.

The radar renderer uses fixed 0–10 radii and the same six-axis order for all eight categories. All six axes have author scores and form a closed, lightly filled polygon. Life impact is subjective author interpretation of potential lasting influence on an engaged person. Research supporting these exact scores or their comparative ordering has not been found in the project review. There is no calibrated procedure translating evidence into these judgments. Point shape distinguishes numeric anchors from qualitative judgments. Both types remain subjective ratings.

The combined `radar-overview.svg` embeds all eight profiles in a 4-by-2 sheet without external image references. Category names, axis labels, scores and brief author-score/marker keys are shown. Detailed explanations remain in adjacent TXT files. The adjacent Russian reading guide, `radar-overview.txt`, is copied from `author-interpretations/radar_overview_annotation.txt` on each rebuild. SVG figures remain in English; the author-interpretation gallery and its README are in Russian.

The overview and individual profiles in the gallery are ordered alphabetically by their displayed English category names, left to right, then top to bottom. This order does not imply a ranking.

The scripts render the current local inputs in English. They do not scrape sources, estimate missing observations or validate author ratings. The music radar also reads `author-interpretations/music_online_scenarios.md` for its dashed streaming-only reference on the first three axes. Historical implementation and input revisions are recorded in [the method archive](../sources/method_history.md) and [score audit](../author-interpretations/subjective_scores_2026.md#revision-rule-and-audit).

All nine radar SVGs and matching TXT files are generated inside `author-interpretations/`. They are excluded from the empirical/context gallery. Validation checks both output directories; Russian text is allowed in documentation and the subjective gallery, while SVG display text stays English.

Snapshot labels implement the distinction between source-format proxies and the separate media-component inventory in `data/media_components_2026.md`. No component uplift is added to a format row. Component totals remain missing and generate no chart. Earlier subjective radars retain their scores with a visible mixed-scope warning; they do not implement the new two-level comparison.

## Local link and section validation

`validate.py` calls `markdown_links.py` to check local Markdown destinations, including `file.md#heading` and same-file `#heading` links. It recognizes ATX/setext heading anchors, duplicate-heading suffixes, Unicode and URL-encoded paths/fragments, reference links, and explicit HTML IDs or named anchors. HTML/SVG target fragments are checked against their explicit anchors. External URL schemes are skipped; links and headings inside fenced code or HTML comments are ignored, as are inline-code links. Failures identify the source file, line, destination and whether the file or anchor is missing.

The checker implements the repository's Markdown conventions and GitHub-style heading slugs, not a full CommonMark renderer. Passing this check establishes local navigation consistency, not correctness of source extraction or evidence.

Run its regression tests with:

```sh
python3 -m unittest discover -s scripts -p 'test_markdown_links.py'
```

## Standalone empirical figure context

Snapshot labels are defined in `SNAPSHOT_LABELS`, separately from author radar names. Source-specific labels include Music streaming and TV streaming (all content); digital books, feature films and standalone pictures are omitted from the images and documented as unavailable in TXT. GWI population/date, metric definition, report page, category details, marker keys and plotted values are in each matching TXT, with an SVG description for accessibility. Reach uses 0–100%, frequency 0–7 days, and daily time is weekly reported minutes divided by seven.

## GMI26 growth chart (Russian)

Run `python3 scripts/build_growth_figure.py` from the project root for the Russian reproduction of chart 573622. The full build also invokes it. Input: [transcribed data](../data/media_growth_h1_2026.md), including source screenshot, method, category mapping and confidence limits. Outputs: `figures/media-growth-h1-2026.svg`, matching TXT and standalone HTML. No external dependencies or network. The Russian growth chart is the explicit exception to the older English-only SVG convention. Percent changes are plotted on a common zero-centered scale; weekly times stay as HH:MM. The original chart's growth period is interpreted from the author transcript, not invented baseline observations.

The growth image contains only a short title/period, category labels, weekly values and the percentage axis. Reading guide, color key, sources, population, method and limitations are in `media-growth-h1-2026.txt`.

## Compact Russian GWI gallery

`python3 scripts/build_gwi_figures.py` generates `figures/gwi/index.html`, with compact Russian reach, weekly-time and frequency SVGs plus per-chart TXT explanations, sources and color keys. The gallery also references the H1 2026 growth chart, built by `build_growth_figure.py`; `build_figures.py` builds both. The existing `figures/` directory is the project's visualization folder. No OUTFRONT historical values are spliced into a growth series. Missing categories are omitted with explanations in TXT. Device-specific game frequencies are not shown as all-game frequency.
