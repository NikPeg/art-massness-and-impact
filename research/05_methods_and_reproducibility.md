# Methods and reproduction

## Research procedure

1. Separate reach, time, frequency, money, cultural recognition, and five kinds of personal impact.
2. Search for public original reports, company disclosures, and research papers. Prefer these over unattributed compilations.
3. Record observation date, population, geography, unit, and reporting vintage.
4. Keep incompatible surveys and narrow industry proxies visibly separate.
5. Preserve gaps instead of interpolating a five-year research result.
6. Add subjective radar judgments only after the user explicitly requested them.

## Transcription and transformations

The Markdown tables in `data/` are the data source for the scripts. `NA` means missing. Annual dollars are stored in billions. BLS hours are stored as reported and multiplied by 60 for the figure. GWI weekly hours and minutes are converted into weekly minutes, then divided by seven for a daily mean. Its frequency values remain days per week, not visits or sessions.

Book fiction revenue is the sum of two AAP categories. Broadway observations are assigned to the calendar year in which a season ends; no adjustment to a 52-week season is made. Source dates and narrow boundaries remain attached to the values.

## Radars

Each radar has the same ten axes, order, and linear 0–10 radius. No normalization against the largest observed revenue or consumption value is used. Scores are frozen in `data/subjective_scores_2026.md`. The distinction between a filled numeric-anchor point and a hollow qualitative point applies to the evidence behind the score, not to whether the score itself is objective.

Rationales are reproduced in `data/score_rationales.md`. Empirical references are deliberately not used to claim that they validate a particular score. The five personal-impact dimensions are conceptual, not measured incidence rates.

## Eighth-category extension

The extension promotes previously retained long-online-video reach/time observations into a labeled proxy row and adds its reported weekly frequency. It defines a narrower horizontal creative-video category, adds ten new subjective scores and rationales without changing the original seven profiles, and preserves five missing financial observations. The generator and checks now cover eight categories and 13 SVGs. Source retrieval and the scope mismatch are recorded in the source register and limitations.

## Participation extension

The user selected Participation Survey and Special Eurobarometer 562 from a wider search. Only those two survey programmes were added. Final sample sizes were checked in technical reports; activity values were transcribed with their source categories into [a separate table file](../data/participation_and_breadth.md). England's earlier wave supplies sample-size context only. No microdata analysis, harmonization, causal estimation, or extrapolation to 2026 was performed. The [participation generator](../scripts/build_participation_figures.py) now reads these tables and produces two figures with TXT annotations, also included in the full gallery build. Existing radar inputs are unaffected. Both percentage axes are fixed at 0-100%; the England connectors compare groups, not time or uncertainty.

## Rendering provenance

The original chat trend chart used D3 7.9.0, responsive SVG, series toggles, and interpolated hover details. Those hover interpolations were visual conveniences, not additional observed data. The original radar fragment used direct SVG geometry with identical scales. Chat charts were visually inspected in a local browser.

This project supplies a fresh English reproduction from the same selected values and radar scores. `scripts/build_figures.py` uses only Python's standard library and writes SVG plus an HTML gallery. It does not scrape sources, estimate missing observations, or call an external service. Differences from the chat interface are layout, language, and interaction; a line is broken at the Newzoo reporting-vintage boundary in both versions.

## Validation

`scripts/validate.py` checks table shape, score bounds, selected numerical anchors, missing-value preservation, generated SVG parsing, local Markdown links, and the presence of all eight radar figures. These checks detect transcription or packaging errors, not whether the research's judgments are true.

To change an empirical input, edit the corresponding Markdown table, update its source or method note, rebuild, and validate. To change a subjective score, also revise its rationale. Do not silently replace a missing observation with an opinion in the empirical tables.
