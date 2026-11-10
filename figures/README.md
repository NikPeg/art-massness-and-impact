# Generated figures

Run `python3 scripts/build_figures.py` from the project root for English output (the default), and `python3 scripts/build_figures.py --lang ru` for Russian output. Both sets coexist. Russian charts and TXT files have the suffix `-ru`; open `index-ru.html` for the fully Russian gallery.

Snapshot SVGs (`reach-2026.svg`, `time-2026.svg`) contain a title, category-axis values and numeric-axis values with units. The reach image also labels each point. Frequency is shown only as the bar chart `gwi/frequency.svg`, with mobile games and PC/console games as separate rows. Matching TXT files contain concise sources, measurement definitions, marker keys and essential caveats, without tables or lists of plotted values. The compact reach/time figure keeps only titles, essential scope labels, axes, units and short annotation references on the image; its matching TXT file provides a short source and measurement caption. The HTML gallery links to each TXT.

- `reach-2026.svg`, `time-2026.svg`: international online-adult snapshot and explicit gaps.
- `reach-time-2026.svg`: exact weekly reach/time coordinates, with displaced labels and leader lines.
- `index.html`: browser gallery of every English SVG in this folder and its subfolders, with matching TXT links. `index-ru.html` contains the matching Russian set. The file list is discovered automatically on each full build.


The Markdown data and research files contain sources, boundaries, and rationales. SVG files are standalone; the HTML gallery has no external dependencies. Generated files may be replaced on a rebuild.

Financial observations remain in [the source table](../data/annual_indicators.md). They are not plotted on a common axis because market coverage, geography, and accounting periods differ.

To rebuild just the compact reach/time figure and its TXT annotation, run `python3 scripts/build_comparison_figures.py`. The full build also generates it and updates the gallery. The scripts use local tables only and require no external Python packages.

Author interpretations, score inputs, and all radial diagrams are in [their own section](../author-interpretations/README.md), with a [separate gallery](../author-interpretations/index.html).

The snapshot charts show broad primary-format proxies, with music streaming, digital books and standalone pictures labeled explicitly. Media components across formats have a [separate evidence inventory](../data/media_components_2026.md); unmeasured component totals are not plotted or inferred from video audiences.

The snapshot uses a 0–100% reach axis, 0–7 days/week frequency axis and a shared 0–75 minutes/day time axis across its rows. Three missing categories are omitted from the images and documented as unavailable in TXT, with no fabricated zero points. TV streaming includes films and other programmes, so it is not labeled as measured series-only use.

## GMI26 growth chart (Russian)

Run `python3 scripts/build_growth_figure.py --lang ru` from the project root for the Russian reproduction of chart 573622. The full build also invokes it. Input: [transcribed data](../data/media_growth_h1_2026.md), including source screenshot, method, category mapping and confidence limits. Outputs: `figures/media-growth-h1-2026.svg`, matching TXT and standalone HTML. No external dependencies or network. Use `--lang ru` for Russian labels; the default output is English. Percent changes are plotted on a common zero-centered scale; weekly times stay as HH:MM. The original chart's growth period is interpreted from the author transcript, not invented baseline observations.

The growth image contains only a short title/period, category labels, weekly values and the percentage axis. Reading guide, color key, sources, population, method and limitations are in `media-growth-h1-2026.txt`.

## Compact Russian GWI gallery

`python3 scripts/build_gwi_figures.py --lang ru` generates `figures/gwi/index-ru.html`, with compact Russian reach, weekly-time and frequency SVGs plus per-chart TXT explanations, sources and color keys. The gallery also references the H1 2026 growth chart, built by `build_growth_figure.py`; `build_figures.py` builds both. The existing `figures/` directory is the project's visualization folder. No OUTFRONT historical values are spliced into a growth series. Missing categories are omitted with explanations in TXT. Device-specific game frequencies are not shown as all-game frequency.
