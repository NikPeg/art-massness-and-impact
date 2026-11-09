# Generated figures

Run `python3 scripts/build_figures.py` from the project root to regenerate these files.

Every SVG has a same-named TXT sidecar containing its annotation, sources, scope notes, and any legend. Images show only chart titles, axis labels, and values. The HTML gallery links to each TXT.

- `us-time-use.svg`: US main-activity minutes per day, 2021–2025.
- `reach-2026.svg`, `time-2026.svg`, `frequency-2026.svg`: international online-adult snapshot and explicit gaps.
- `radar-*.svg`: eight subjective 2026 profiles.
- `radar-pictures.svg`: Pictures profile, with qualitative markers on every axis and no matched numeric consumption or revenue anchors.
- `radar-long-video.svg`: the added horizontal creative-video profile; broader consumption proxies and no numeric money anchor.
- `radar-overview.svg`: all eight radar profiles in one standalone 4-by-2 sheet, with identical axes and scales.
- `radar-overview.txt`: short Russian reading guide and definitions of all six axes, including the unassessed general Life impact axis. Its editable source is `data/radar_overview_annotation.txt`.
- `index.html`: English browser gallery with all figures and evidence notes.
- `active-participation-eu-2025.svg`: selected active artistic activities, EU27, with an overall rate separated above them.
- `social-breadth-england-2024-25.svg`: physical and digital participation by area-deprivation extremes, England; connected pairs on a 0-100% scale.

The two participation SVGs have adjacent same-named TXT files. Regenerate them independently with `python3 scripts/build_participation_figures.py`, or regenerate the complete gallery with the main command above.

The Markdown data and research files contain sources, boundaries, and rationales. SVG files are standalone; the HTML gallery has no external dependencies. Generated files may be replaced on a rebuild.

Financial observations remain in [the source table](../data/annual_indicators.md). They are not plotted on a common axis because market coverage, geography, and accounting periods differ.
