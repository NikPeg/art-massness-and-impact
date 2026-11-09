# Reproduction and validation

## Current package, 9 November 2026

The project covers eight categories of internet-distributed media content. Inputs contain 40 financial cells (including missing values), eight 2026 snapshot rows, 48 subjective radar scores and 48 rationale entries. The full build produces 13 SVGs and two separate HTML galleries: eight individual radars and one overview in the author-interpretation folder, four consumption-context figures. Financial context remains in tables without a common chart.

All radars have six scored axes, including general Life impact. Scores illustrate author judgments; they are not empirical estimates or research findings. Music has a separate dashed streaming-only reference alongside its inclusive-online profile. Pictures have no matched empirical consumption/revenue observations or numerical radar anchors.

## Checks

Run from the project root:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

The validator checks categories/counts, selected source observations, missing values, score bounds, rationale coverage, music scenario consistency, qualitative pictures data markers, 29 question/answer IDs, SVG syntax, overview panels, accessibility IDs, label bounds, TXT annotations, local Markdown file links and English figure text. A source-anchor legend circle is distinct from a data marker.

The full build and validator passed for the current documentation consolidation on 9 November 2026. Documentation links and whitespace were checked separately. No empirical observation, radar score or rendering rule was changed by that consolidation.

## Hypothesis applicability audit

All 29 answers were assessed against the same content/distribution, exposure, population, comparator, outcome/follow-up and causal-design criteria. Each answer row now records its scope fit. H12, H18, H22 and H29 remain unanswered; H23 is unanswered without a retained matched online-format comparison, and H04/H05 are partial publisher-proxy comparisons. No substantive answer currently meets the full-scope rule. Confidence is attached to bounded supported findings, not used to repair a scope mismatch. The audit changes classifications and prose, not underlying data or author scores.

## Limits of verification

Automated checks establish structural consistency and packaging. They do not validate source producers' data, literature completeness, causal conclusions or author scores; local file checks do not test external URLs or every section anchor. Historical visual checks covered selected figures and earlier versions; they do not certify every current figure or this documentation revision. No new visual inspection is claimed for this revision.

Detailed past runs, visual checks and superseded failures are retained in [the validation archive](../sources/validation_history.md). The [methods](../research/05_methods_and_reproducibility.md) describe the current workflow. This remains an exploratory dossier, not a validated causal ranking of media.

## Format and component separation, 9 November 2026

Regenerated both galleries and all SVG/TXT outputs after separating primary work formats from cross-format media components. Snapshot values and author scores were not changed. Snapshot labels now name music streaming, digital books and standalone pictures explicitly; earlier author profiles visibly warn that they mix comparison levels. A separate four-component inventory retains NA for every unmeasured reach/time/frequency total. The generator does not render a component ranking from those gaps.

`python3 scripts/build_figures.py` and `python3 scripts/validate.py` passed. The validator checks the component rows and missing totals, explicit snapshot labels, existing table values, SVG structure and local Markdown links. These checks do not validate the source proxies as item-level primary-format measurements, establish component audiences or isolate causal effects. No pixel-level visual inspection is claimed for this update.

## Local section-anchor validation, 9 November 2026

`validate.py` now checks fragments as well as destination-file existence through `scripts/markdown_links.py`. It checks same-file and cross-file Markdown heading anchors, duplicate suffixes, reference links, Unicode/URL encoding, and explicit HTML anchors; code examples and comments are excluded under the documented conventions. Missing targets report source file, line, destination and reason. This is a repository-convention checker, not a complete Markdown renderer or an extraction audit.

All eight regression tests passed, including rejection of an existing file linked with a renamed `#ten-dimensions` heading. The current Markdown corpus contains no remaining occurrence of that obsolete fragment. The final full-package validation correctly failed on an existing link in `sources/balanced_review_search_2026.md` to the absent `research/09_balanced_literature_review.md`. That separate source/synthesis work was not rewritten or replaced with a placeholder by this validator change.

## Standalone empirical labels and visual inspection, 9 November 2026

Rebuilt all four empirical SVGs with source-specific category labels, explicit missing observations, visible population/period/source notes and metric definitions. Snapshot reach/frequency axes use their full 0–100% and 0–7 bounds. The BLS diary image visibly identifies broad activities, all-person daily means and offline coverage. Empirical input values and author scores did not change.

Rendered reach, daily time, frequency and US time-use SVGs to PNG with the bundled Sharp renderer and inspected all four images. Category labels, missing-value text, point values, game-device legend, tick labels and footnotes were visible without clipping or overlap. The full validator and whitespace checks passed. Additional checks require visible source/population notes and three explicit snapshot gaps; these establish packaging, not source-data validity. This visual check covers the four empirical images, not the separate author radars.
