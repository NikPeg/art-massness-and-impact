# Reproduction and validation

## Current package, 9 November 2026

The project covers eight categories of internet-distributed creative content. Inputs contain 40 financial cells (including missing values), eight 2026 snapshot rows, 48 subjective radar scores and 48 rationale entries. The full build produces 15 SVGs and an HTML gallery: eight individual radars, one overview, four consumption-context figures and two participation figures. Financial context remains in tables without a common chart.

All radars have six scored axes, including general Life impact. Scores illustrate author judgments; they are not empirical estimates or research findings. Music has a separate dashed streaming-only reference alongside its inclusive-online profile. Pictures have no matched empirical consumption/revenue observations or numerical radar anchors.

## Checks

Run from the project root:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

The validator checks categories/counts, selected source observations, missing values, score bounds, rationale coverage, music scenario consistency, qualitative pictures data markers, 27 question/answer IDs, SVG syntax, overview panels, accessibility IDs, label bounds, participation values/scales, TXT annotations, local Markdown file links and English figure text. A source-anchor legend circle is distinct from a data marker.

The full build and validator passed for the current documentation consolidation on 9 November 2026. Documentation links and whitespace were checked separately. No empirical observation, radar score or rendering rule was changed by that consolidation.

## Limits of verification

Automated checks establish structural consistency and packaging. They do not validate source producers' data, literature completeness, causal conclusions or author scores; local file checks do not test external URLs or every section anchor. Historical visual checks covered selected figures and earlier versions; they do not certify every current figure or this documentation revision. No new visual inspection is claimed for this revision.

Detailed past runs, visual checks and superseded failures are retained in [the validation archive](../sources/validation_history.md). The [methods](../research/05_methods_and_reproducibility.md) describe the current workflow. This remains an exploratory dossier, not a validated causal ranking of media.
