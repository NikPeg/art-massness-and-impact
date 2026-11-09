# Reproduction scripts

The authoritative inputs are Markdown tables under `../data/`.

- `build_figures.py`: reads those tables, converts selected units, and writes English SVG figures and `figures/index.html`.
- Each SVG has a matching TXT annotation generated alongside it. Chart images retain only titles, axis labels, and values; explanatory text and color/marker legends are in the TXT files, linked from the gallery.
- `validate.py`: checks selected values, missing observations, score bounds, eight radar outputs and their combined overview, SVG syntax, and local Markdown links.

Run both with Python 3.9+. No pip packages, browser libraries, external chart CDN, network requests, or credentials are used.

The time-series renderer preserves missing observations. It never connects the 2025 games estimate to the 2022–2024 reporting vintage. The Reels point is a diamond representing an annualized lower-bound landmark. Theater uses seasonal observations by ending year.

The radar renderer uses fixed 0–10 radii and the same axis order for all eight categories. Point shape distinguishes numeric anchors from qualitative judgments. Both types remain subjective ratings.

The combined `radar-overview.svg` embeds all eight profiles in a 4-by-2 sheet without external image references. Category names, axis labels, and scores are shown; the overall heading, subtitles, legends, and explanatory footers are omitted. The adjacent Russian reading guide, `radar-overview.txt`, is copied from `data/radar_overview_annotation.txt` on each rebuild. Figures and the gallery remain in English.

The overview is ordered by descending polygon area, left to right, then top to bottom. Area is proportional to the cyclic sum of products of adjacent axis scores. This geometric layout does not define an overall impact ranking.

These scripts are the English reproduction used to generate this project's figures. The original chat implementations used D3 for time series and direct SVG for radars; their hover interactions and styling are not reproduced byte-for-byte. No empirical estimates or radar scores were refitted in the migration.
