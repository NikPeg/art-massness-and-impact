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

Book fiction revenue is the sum of two AAP categories. Source dates and narrow boundaries remain attached to the values. Financial observations are retained as tables only: their incompatible market and accounting scopes cannot support a common monetary axis.

## Radars

Each radar has the same six axes and order: reach, time, frequency, money, recognition, and general Life impact. Only the first five have subjective 0–10 scores. Life impact is NA for every category; its marker is omitted, and the profile remains open and unfilled. Former detailed impact scores were removed without averaging or transferring them. Panels follow alphabetical category order rather than polygon area. No normalization against the largest observed revenue or consumption value is used. Current revised scores are recorded in `data/subjective_scores_2026.md`. The distinction between a filled numeric-anchor point and a hollow qualitative point applies to the evidence behind the score, not to whether the score itself is objective.

Rationales are reproduced in `data/score_rationales.md`. Empirical references are deliberately not used to claim that they validate a particular score. The general Life impact axis is a conceptual placeholder, with no numerical estimate or comparative ranking.

## Long-video category

The extension promotes previously retained long-online-video reach/time observations into a labeled proxy row and adds its reported weekly frequency. It defines a narrower horizontal creative-video category, adds ten new subjective scores and rationales without changing the other six retained profiles, and preserves five missing financial observations. The generator and checks now cover eight categories and 15 SVGs including the overview and participation charts. Source retrieval and the scope mismatch are recorded in the source register and limitations.

## Participation extension

The user selected Participation Survey and Special Eurobarometer 562 from a wider search. Only those two survey programmes were added. Final sample sizes were checked in technical reports; activity values were transcribed with their source categories into [a separate table file](../data/participation_and_breadth.md). England's earlier wave supplies sample-size context only. No microdata analysis, harmonization, causal estimation, or extrapolation to 2026 was performed. The [participation generator](../scripts/build_participation_figures.py) now reads these tables and produces two figures with TXT annotations, also included in the full gallery build. Existing radar inputs are unaffected. Both percentage axes are fixed at 0-100%; the England connectors compare groups, not time or uncertainty.

## Rendering provenance

The original chat trend chart used D3 7.9.0, responsive SVG, series toggles, and interpolated hover details. Those hover interpolations were visual conveniences, not additional observed data. The original radar fragment used direct SVG geometry with identical scales. Chat charts were visually inspected in a local browser.

This project supplies a fresh English reproduction from the selected observations and current versioned-in-Git radar judgments. `scripts/build_figures.py` uses only Python's standard library and writes SVG plus an HTML gallery. It does not scrape sources, estimate missing observations, or call an external service. Differences from the chat interface are layout, language, and interaction; a line is broken at the Newzoo reporting-vintage boundary in both versions.

## Validation

`scripts/validate.py` checks table shape, score bounds, selected numerical anchors, missing-value preservation, generated SVG parsing, local Markdown links, and the presence of all eight radar figures. These checks detect transcription or packaging errors, not whether the research's judgments are true.

To change an empirical input, edit the corresponding Markdown table, update its source or method note, rebuild, and validate. To change a subjective score, also revise its rationale. Do not silently replace a missing observation with an opinion in the empirical tables.

## Pictures extension, 9 November 2026

Added a working pictures definition and five primary research/report sources from 2024–2026, with retrieval levels recorded. The literature review separates memory, attention, viewing experience, and creation. Main-type creation shares remain in a separate table with their conditional denominator; no GWI values or revenue estimates are inferred from them.

Added eight-category inputs: one all-NA snapshot row, five all-NA financial cells, ten subjective scores and rationales, and all-NA numeric-anchor flags for pictures. The other seven score rows are unchanged. Regenerated all figures, the eight-panel overview, annotations, and gallery. The current total is 15 SVGs after removal of the common financial chart. Updated count, category, gap, and rationale checks. No new radar axis or empirical normalization was introduced.

## Online-scope revision, 9 November 2026

Reviewed the first four axes of all eight profiles, updated 22 scores, and removed incompatible whole-market/offline numerical anchor flags. Pictures retain their prior values. Recognition retains its author hypothesis after checking the online interpretation; the current general Life impact axis remains unassessed. The [revision audit](../data/subjective_scores_2026.md#revision-rule-and-audit) gives every before/after value. These remain ordinal judgments with no data-to-score formula.

For music, the main profile covers direct and embedded online audible contact. A [separate scenario table](../data/music_online_scenarios.md) supplies a streaming-only reference drawn as a dashed segment on its first three axes. This records a change of exposure definition, not a fitted uplift. Embedded musical contact counts substantively, while unique people, intervals and days require within-music unions. No measured combined audience is inferred. Musical effects within video are not causally separated from other components. Original empirical tables and contextual figures retain their observations. Regenerated the gallery and all figures from the revised inputs.
