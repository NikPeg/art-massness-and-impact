# Historical method and implementation notes

Archived on 9 November 2026. These entries describe intermediate project versions, not the current methods, category counts, radar axes or validation status. Some statements were superseded by later work. Use [current methods](../research/05_methods_and_reproducibility.md), [current validation](../results/04_validation.md) and the [search log](research_log.md) for the present package and source access.

## Long-video category

The extension promotes previously retained long-online-video reach/time observations into a labeled proxy row and adds its reported weekly frequency. It defines a narrower horizontal creative-video category, adds ten new subjective scores and rationales without changing the other six retained profiles, and preserves five missing financial observations. The generator and checks now cover eight categories and 15 SVGs including the overview and participation charts. Source retrieval and the scope mismatch are recorded in the source register and limitations.

## Participation extension

The user selected Participation Survey and Special Eurobarometer 562 from a wider search. Only those two survey programmes were added. Final sample sizes were checked in technical reports; activity values were transcribed with their source categories into [a separate table file](../data/participation_and_breadth.md). England's earlier wave supplies sample-size context only. No microdata analysis, harmonization, causal estimation, or extrapolation to 2026 was performed. The [participation generator](../scripts/build_participation_figures.py) now reads these tables and produces two figures with TXT annotations, also included in the full gallery build. Existing radar inputs are unaffected. Both percentage axes are fixed at 0-100%; the England connectors compare groups, not time or uncertainty.

## Rendering provenance

The original chat trend chart used D3 7.9.0, responsive SVG, series toggles, and interpolated hover details. Those hover interpolations were visual conveniences, not additional observed data. The original radar fragment used direct SVG geometry with identical scales. Chat charts were visually inspected in a local browser.

This project supplies a fresh English reproduction from the selected observations and current versioned-in-Git radar judgments. `scripts/build_figures.py` uses only Python's standard library and writes SVG plus an HTML gallery. It does not scrape sources, estimate missing observations, or call an external service. Differences from the chat interface are layout, language, and interaction; a line is broken at the Newzoo reporting-vintage boundary in both versions.

## Pictures extension, 9 November 2026

Added a working pictures definition and five primary research/report sources from 2024–2026, with retrieval levels recorded. The literature review separates memory, attention, viewing experience, and creation. Main-type creation shares remain in a separate table with their conditional denominator; no GWI values or revenue estimates are inferred from them.

Added eight-category inputs: one all-NA snapshot row, five all-NA financial cells, ten subjective scores and rationales, and all-NA numeric-anchor flags for pictures. The other seven score rows are unchanged. Regenerated all figures, the eight-panel overview, annotations, and gallery. The current total is 15 SVGs after removal of the common financial chart. Updated count, category, gap, and rationale checks. No new radar axis or empirical normalization was introduced.

## Online-scope revision, 9 November 2026

Reviewed the first four axes of all eight profiles, updated 22 scores, and removed incompatible whole-market/offline numerical anchor flags. Pictures retain their prior values. Recognition retains its author hypothesis after checking the online interpretation; the general Life impact axis subsequently received separate subjective author scores at the user's request. The [revision audit](../data/subjective_scores_2026.md#revision-rule-and-audit) gives every before/after value. These remain ordinal judgments with no data-to-score formula.

For music, the main profile covers direct and embedded online audible contact. A [separate scenario table](../data/music_online_scenarios.md) supplies a streaming-only reference drawn as a dashed segment on its first three axes. This records a change of exposure definition, not a fitted uplift. Embedded musical contact counts substantively, while unique people, intervals and days require within-music unions. No measured combined audience is inferred. Musical effects within video are not causally separated from other components. Original empirical tables and contextual figures retain their observations. Regenerated the gallery and all figures from the revised inputs.

## Everyday and cumulative outcomes extension, 9 November 2026

A targeted search added seven original studies spanning everyday affect regulation, image-exposure trajectories, mixed-platform diaries, timescale-dependent stress associations, friendship-closeness follow-up, sharing habits and perceived norms. Retrieval levels are recorded in the source register and dedicated appraisal. Norm-change radio evidence is contextual and outside online distribution. Two recent diary papers are treated as potentially sharing a sample, not independent replications. No pooled effect, cross-medium score, or causal cumulative estimate was calculated.

Revised the central definition and prospective protocol to report major events separately from everyday/cumulative changes, including null/mixed findings and post-exposure persistence as a separate test. No empirical figure input or radar value was changed by this literature extension.
