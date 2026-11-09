# Art, mass reach, and life impact

An exploratory research dossier, prepared on **9 November 2026**. All prose is in Markdown. Figures and executable reproduction scripts are stored separately. No LaTeX or paid datasets are required.

## Research question

Has short-form vertical video become the most mass-consumed art form, and does that also make it the most influential in people's lives?

**Finding:** short video has exceptionally broad reach and frequent use in the available online-adult survey. Absolute leadership across art forms is not established. Attention, commercial scale, durable cultural recognition, and life-changing influence are different outcomes. No comparable global series measures major life changes caused by all eight forms.

## Read first

- [Findings](results/01_findings.md): conclusions and empirical figures.
- [Social breadth and active participation](data/participation_and_breadth.md): selected England and EU surveys, with observation dates and methodological limits.
- [Radar profiles](results/02_radar_profiles.md): eight explicitly subjective profiles for 2026.
- [All radar profiles in one image](figures/radar-overview.svg), with a [short Russian annotation (TXT)](figures/radar-overview.txt).
- [Literature review](research/02_literature_review.md): what research on meaningful experiences, persuasion, and behavior actually measures.
- [Source comparison](research/03_source_comparison.md): incompatible denominators, reporting vintages, and financial boundaries.
- [Limitations](research/04_limitations.md): overlap, causality, missing series, and radar assumptions.

## Contents

```text
research/    Scope, literature, source comparison, limitations, methods
sources/     Source register and search/audit log
data/        Observations, subjective scores, and score rationales in Markdown
scripts/     Standard-library Python figure generator and validation
figures/     Generated SVG figures and an English HTML gallery
results/     Findings, radar interpretation, and proposed next study
```

The eight categories are short-form video, long-form horizontal online video, music, feature films, series, books, staged plays, and video games. They overlap and are not a complete taxonomy of art. The added long-video category covers creator-led horizontal creative works, separately from feature films and scripted series. Its survey anchors are broader long-online-video proxies; financial observations remain missing. See the [working definition](research/01_scope_and_metrics.md#long-form-horizontal-online-video) and [additional limitations](research/04_limitations.md#additional-limitations-introduced-by-long-horizontal-video).

## Reproduce

Run from this directory with Python 3.9 or newer:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

Open `figures/index.html` in a browser. The generated figures use no external libraries or network requests. The source data are editable Markdown tables. A rerun replaces only generated files in `figures/`.

## Evidence labels

- **Observation:** a source reports this value for a specified population and period.
- **Proxy:** a related measure, such as Netflix revenue for a broader discussion of series.
- **Subjective score:** an author-assigned 0–10 judgment; sources do not report the score.
- **Gap:** no comparable observation was selected. A gap is not zero.

The 2021–2025 financial series combine different market boundaries. The US time-use series is kept separate from the international 2026 snapshot. Neither is a universal league table. In the radar figures, even a score with a numeric anchor remains subjective.

## Provenance

This dossier consolidates the research and visualizations developed in the accompanying conversation. Original chat charts used D3 7.9.0 for time series and handwritten SVG for radars. The scripts here reproduce their observations and frozen radar scores in English using deterministic, dependency-free SVG generation; they are not byte-identical copies of the chat interface. See [methods](research/05_methods_and_reproducibility.md) and [script notes](scripts/README.md).

Published numbers were transcribed from the linked sources; original survey microdata and publisher accounting records were not obtained. This is a targeted review, not a systematic review or a new causal study.
