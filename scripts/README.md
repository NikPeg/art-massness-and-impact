# Reproduction scripts

The authoritative inputs are Markdown tables under `../data/`.

- `build_figures.py`: reads those tables, converts selected units, and writes English SVG figures and `figures/index.html`.
- `build_participation_figures.py`: independently generates the EU active-participation and England social-breadth SVGs with adjacent TXT annotations. Also called by `build_figures.py`, which includes them in the gallery.
- `validate_participation_figures.py`: independently checks displayed percentages against the source tables, 0-100% scales, label coordinates, and annotations. Also called by `validate.py`.
- Each SVG has a matching TXT annotation generated alongside it. Images retain brief color/marker keys and radars visibly identify author scores. Explanations and sources are in the adjacent TXT files, linked from the gallery.
- `validate.py`: checks selected values, missing observations, score bounds, eight radar outputs and their combined overview, SVG syntax, and local Markdown links.

Run both with Python 3.9+. No pip packages, browser libraries, external chart CDN, network requests, or credentials are used.

To regenerate only the two participation figures:

```sh
python3 scripts/build_participation_figures.py
python3 scripts/validate_participation_figures.py
```

Participation inputs come from `data/participation_and_breadth.md`. EU activities use horizontal dots with the overall participation rate separated above the selected activities. England uses connected pairs for the most and least deprived areas. Both scales run from 0 to 100%; notes and the pair-marker legend are in TXT files. Survey years remain in chart titles. These are observations, not radar judgments.

The common financial chart has been removed: market totals, company revenue, cinema gross, and an annualized revenue pace cannot support a shared commercial-scale comparison. Financial observations remain in the source tables. The build removes the obsolete financial SVG and TXT outputs and excludes them from the gallery. The time-series renderer is used for US time use.

The radar renderer uses fixed 0–10 radii and the same six-axis order for all eight categories. All six axes have author scores and form a closed, lightly filled polygon. Life impact is subjective author interpretation of potential lasting influence on an engaged person. Research supporting these exact scores or their comparative ordering has not been found in the project review. These are fresh judgments requested by the user, not averages of the former detailed axes. Point shape distinguishes numeric anchors from qualitative judgments. Both types remain subjective ratings.

The combined `radar-overview.svg` embeds all eight profiles in a 4-by-2 sheet without external image references. Category names, axis labels, and scores are shown; the overall heading, subtitles, legends, and explanatory footers are omitted. The adjacent Russian reading guide, `radar-overview.txt`, is copied from `data/radar_overview_annotation.txt` on each rebuild. Figures and the gallery remain in English.

The overview and individual profiles in the gallery are ordered alphabetically by their displayed English category names, left to right, then top to bottom. This order does not imply a ranking.

These scripts are the English reproduction used to generate this project's figures. The original chat implementations used D3 for time series and direct SVG for radars; their hover interactions and styling are not reproduced byte-for-byte. No empirical estimates or radar scores were refitted in the original migration. The subsequent online-scope revision changes author scores and anchor flags, documented in the score audit; it does not change empirical observations. The music radar also reads `data/music_online_scenarios.md` for a dashed streaming-only reference on its first three axes.
