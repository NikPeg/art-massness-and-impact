# Reproduction scripts

Empirical inputs are Markdown tables under `../data/`. Author scores, rationales, music scenarios and the editable radar annotation are under `../author-interpretations/`.

- `build_figures.py`: reads those tables, converts selected units, and writes empirical/context SVGs and `figures/index.html`, plus radar SVGs and a separate `author-interpretations/index.html` gallery.
- Each SVG has a matching TXT annotation generated alongside it. Empirical images include precise source-category labels, missing-data notices, population, period, source and essential scope notes. TXT files carry extended explanations. Radars visibly identify author scores.
- `validate.py`: checks selected values, missing observations, score bounds, eight radar outputs and their combined overview, SVG syntax, and both files and section anchors in local Markdown links.

Run both with Python 3.9+. No pip packages, browser libraries, external chart CDN, network requests, or credentials are used.

The common financial chart has been removed: market totals, company revenue, cinema gross, and an annualized revenue pace cannot support a shared commercial-scale comparison. Financial observations remain in the source tables. The build removes the obsolete financial SVG and TXT outputs and excludes them from the gallery. The time-series renderer is used for US time use.

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

Snapshot labels are defined in `SNAPSHOT_LABELS`, separately from author radar names. Source-specific labels include Music streaming and TV streaming (all content); digital books, feature films and standalone pictures carry explicit unavailable notices. GWI population/date, metric definition and report page are visible inside each SVG, with a description for accessibility. Reach uses 0–100%, frequency 0–7 days, and daily time is weekly reported minutes divided by seven. The US diary chart visibly states its BLS source, all-person main-activity denominator and offline coverage.
