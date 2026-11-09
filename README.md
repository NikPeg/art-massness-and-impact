# Internet-distributed media: mass reach, participation, and life impact

A research dossier based on a **moderate targeted literature review**, updated on **9 November 2026**. All prose is in Markdown. Figures and executable reproduction scripts are stored separately. No LaTeX or paid datasets are required.

## Research question

The project examines reach, consumption growth, participation, and life impact of media distributed through the internet. All research questions and interpretive hypotheses are collected in [Project hypotheses](research/06_hypotheses.md); numbered answers and confidence assessments are in [Findings](results/01_findings.md#answers-to-the-project-hypotheses).

**Finding:** short video has exceptionally broad reach and frequent use in the available online-adult survey. Additional sources give moderate confidence in growth of short-video services within several measured audiences. The inspected GMI26 chart supports moderate confidence in a bounded comparative finding: short video has the largest reported percentage growth among 12 categories (+5.2%, H1 2026). Population is internet users aged 16–64; the author discussion identifies year-on-year growth. Statistical uncertainty and matched-wave comparability remain unaudited. See the [transcribed chart](data/media_growth_h1_2026.md). Absolute leadership across all eight media in consumption or growth is not established. Attention, commercial scale, durable cultural recognition, and life-changing influence are different outcomes. No comparable global series measures major life changes caused by all eight categories.

## Review status and search limits

The literature component is a **moderate targeted review with matched outcome searches across all eight media formats**. The corrective search adds 24 common-block queries, eight synonym queries and 18 source-retrieval/gap searches. It replaces the earlier assignment of different outcomes to different categories with a common evidence matrix. New appraisals retain positive, null and mixed results; irrelevant leads are removed from the main influence synthesis. This is a documented bounded review, not a systematic review or evidence that all categories are equally well studied. No independent screening or formal risk-of-bias assessment was completed.

See the [matched search and decisions](sources/balanced_review_search_2026.md), [eight-format evidence matrix and new appraisals](research/09_balanced_literature_review.md), [earlier search record](sources/moderate_review_search_2026.md), and [limitations](research/04_limitations.md#literature-search-coverage-and-confidence). The same outcome families are searched for each category, but incompatible exposures, populations, instruments and follow-ups still prevent a medium ranking. “Not found in this search” does not mean “no studies exist.” Search coverage and confidence in a specified conclusion remain separate.

Hypothesis answers use one [scope-fit rule](research/05_methods_and_reproducibility.md#hypothesis-answer-status-and-scope-fit): substantive answers must address the original online media-content question; partial answers identify the narrower result or proxy; contextual mechanisms alone leave the hypothesis unanswered. Status and confidence are separate. The findings record scope limits for each of H01–H29.

The [further-work plan](FURTHER_WORK.md) describes how to advance to a full systematic review and, if still needed, a new causal comparison.

## Read first

- [Project hypotheses](research/06_hypotheses.md): questions only, without results or evidence assessments.
- [Findings](results/01_findings.md): conclusions and empirical figures.
- [Media components](data/media_components_2026.md): separate cross-format comparison, coding example and measurement gaps.
- [Growth feasibility](results/05_growth_feasibility.md): updated confidence, independent service-use measurements, the attributed GMI26 growth finding, and remaining comparability checks.
- [Growth evidence search](research/08_growth_evidence_search.md): source appraisals, retrieval limits, and additional leads.
- [Major events and cumulative changes](results/06_event_and_cumulative_outcomes.md): separate results for everyday influence, with [study appraisals](research/08_cumulative_media_effects.md).
- [Author interpretations](author-interpretations/README.md): subjective conclusions based on the project's research and statistics, with a [separate radar gallery](author-interpretations/index.html).
- [Radar profiles](author-interpretations/02_radar_profiles.md): eight explicitly subjective profiles for 2026.
- [All radar profiles in one image](author-interpretations/radar-overview.svg), with a [short Russian annotation (TXT)](author-interpretations/radar-overview.txt).
- [Literature review](research/02_literature_review.md): what research on meaningful experiences, persuasion, and behavior actually measures.
- [Source comparison](research/03_source_comparison.md): incompatible denominators, reporting vintages, and financial boundaries.
- [Limitations](research/04_limitations.md): search coverage, overlap, causality, missing series, and radar assumptions.
- [Further work](FURTHER_WORK.md): steps and completion criteria for a full systematic review and a separate primary study.

## Contents

```text
research/    Scope, literature, source comparison, limitations, methods
sources/     Source register and search/audit log
data/        Source observations in Markdown
scripts/     Standard-library Python figure generator and validation
figures/     Empirical/context SVG figures and their HTML gallery
author-interpretations/ Author interpretations, scores, rationales, and radar gallery
results/     Research findings and proposed next study
```

The project compares eight online media categories: short video, long video, music, feature films, series, digital books, video games and pictures. Entertainment, news, instructions, advertising and personal content are all within scope. Findings use the media categories actually measured by each source. TV streaming remains a proxy for series; source video categories do not establish vertical or horizontal orientation. The [scope](research/01_scope_and_metrics.md) separates primary formats from embedded media components without assigning an exclusive attention budget.

## Reproduce

Run from this directory with Python 3.9 or newer:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

Open `figures/index.html` in a browser. The generated figures use no external libraries or network requests. The source data are editable Markdown tables. Author interpretations have their own gallery at `author-interpretations/index.html`. A rerun replaces generated files in `figures/` and `author-interpretations/`.

## Evidence labels

- **Observation:** a source reports this value for a specified population and period.
- **Proxy:** a related measure, such as Netflix revenue for a broader discussion of series.
- **Subjective score:** an author-assigned 0–10 judgment; sources do not report the score.
- **Gap:** no comparable observation was selected. A gap is not zero.

The 2021–2025 financial observations have different market boundaries. Financial values remain in the source tables without a chart. The compact reach/time scatter has a detailed adjacent TXT annotation and is generated by `scripts/build_comparison_figures.py`, also called by the full build. The US time-use series is kept separate from the international 2026 snapshot. Neither is a universal league table. In the radar figures, even a score with a numeric anchor remains subjective.

## Methods and provenance

The [methods](research/05_methods_and_reproducibility.md) describe the current eight-category project. The [script notes](scripts/README.md) explain deterministic, dependency-free figure generation from local tables. Historical implementation and verification details are kept separately in the [method archive](sources/method_history.md), [validation archive](sources/validation_history.md) and [research log](sources/research_log.md).

Published numbers were transcribed from the linked sources; original survey microdata and publisher accounting records were not obtained. This is a documented targeted review with the search limits stated above, not a systematic review or a new causal study.

[Графики GWI на русском: охват, время, частота и рост](figures/gwi/index.html). Краткие подписи на изображениях; источники, легенды и ограничения — в TXT рядом.
