# Historical validation records

These records concern successive versions and include superseded configurations and failures. They do not describe current status. See [current validation](../results/04_validation.md). Relative links in the archived text retain the same sibling depth as the original results file.

# Reproduction and validation record

## Current eight-category package, 9 November 2026

The target scope is creative content distributed through the internet. The full build produces 15 SVGs and the HTML gallery: eight individual radar profiles, one radar overview, four consumption context figures, and two participation figures. The data contain 40 financial cells, eight snapshot rows, and 48 subjective numeric scores, including eight author Life impact judgments, and 48 corresponding rationale entries. Radar consumption and money judgments have now been revised for online-only use; contextual empirical observations retain their original scopes. Music includes substantive embedded online musical contact, with a separately labeled streaming-only reference.

Commands run from the project root:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

Both commands passed after the radar simplification. The validator also checks pictures-only gaps, hollow markers, and 27 question/answer IDs.

The validator checks table categories and counts, selected observations, score bounds, rationale coverage, SVG syntax, overview panels, accessibility IDs, snapshot label bounds, participation values and scales, TXT annotations, local Markdown links, and English figure text. Structural checks do not establish pixel-level layout quality or validate subjective judgments and source producers' data. Scripts contain no network dependencies.

Visually inspected the pictures radar, complete eight-panel overview, and updated reach chart in a browser through a temporary loopback server. Labels, values, and hollow markers were visible without clipping. The pictures row was present without a fabricated observation. Other figures received structural checks; no new visual inspection of those figures is claimed.

The project is a reproducible exploratory dossier, not a validated causal ranking of creative media.

## Social-breadth hypothesis extension

After adding H27 and its source assessment, `python3 scripts/validate.py` passed on 9 November 2026. No empirical figure inputs or radar scores changed; no new figure build or visual inspection was required.

## Radar simplification, 9 November 2026

Removed the five detailed personal-impact axes and their numerical scores. General Life impact is NA for every category; no scores were transferred or averaged. The generator leaves the profile open and unfilled, and the overview follows alphabetical category order. Updated rationale and missing-value validation; rebuilt all figures and ran the full validator. The visual inspection described above predates this revision.

## Removal of the common financial chart

Removed the financial SVG and annotation, its gallery entry, and its embedding in the findings. Financial source observations remain in the Markdown tables. The generator removes obsolete financial outputs on rebuild. The full build and validator passed after this removal; no chart geometry or empirical values changed.

## Online-scope score revision

Rebuilt the current gallery after revising 22 consumption/money author scores and removing incompatible numeric anchor flags. Added a data-driven streaming-only reference segment on the music radar, alongside the qualitative inclusive-online music profile. The validator checks that the inclusive scenario matches the main profile, that its consumption/money markers remain qualitative, that the dashed reference exists, and that whole-market revenues do not reappear as numeric anchors.

The full build and validator passed on 9 November 2026. Rendered the music radar and complete overview to PNG with the bundled Sharp SVG renderer and visually inspected them. Moved the streaming-reference caption below the money-axis score to prevent overlap. This checks rendering and consistency, not the validity of the subjective point choices.

## Subjective Life impact completion, 9 November 2026

At the user's request, assigned Life impact scores of 5/8/8/8/8/9/8/6 in source-table category order. Life impact is subjective author interpretation of potential lasting influence on an engaged person. Research supporting these exact scores or their comparative ordering has not been found in the project review. These are fresh judgments requested by the user, not averages of the former detailed axes. Profiles are now closed and lightly filled. Updated SVG descriptions, Russian annotations, gallery notes, rationales, and score validation.

## Everyday and cumulative influence literature extension

On 9 November 2026, added a seven-study appraisal, a separate event/everyday-results report, source-register and research-log entries, and revised scope, limitations and proposed methods. Ran `python3 scripts/validate.py` and `git diff --check`; both passed. The extension changes research prose only. No empirical chart input or radar score changed; no new figure build or visual inspection is claimed for this extension.

## Consumption-growth evidence update, 9 November 2026

Added GMI26, IRIS25, QUST25 and GWI method documentation to the source register and research log, with access limits and discovery-only leads recorded separately. Updated the growth assessment, H04/H05 answers, README and limitations. Confidence is moderate only for service growth within several measured audiences; comparative hypotheses remain low-confidence and tentative. The cross-release arithmetic no longer supplies a directional growth inference.

`python3 scripts/validate.py` initially passed after the documentation update. A subsequent final run failed the existing pictures-radar assertion: it rejects every circle, including the source-anchor legend circle now present in that SVG. This documentation update did not change the generator, figures or validator. The final full-package check is therefore not clean. Separately checked the new internal section links and removed references to the superseded provisional-comparison heading; the targeted documentation checks passed.

## Moderate literature-review documentation, 9 November 2026

Added the eight-query targeted-search and selected-candidate register, outcome-specific literature update, explicit README status, search limitations, confidence definition and FURTHER_WORK.md. The full project validator passed after these documentation changes, including local Markdown links. No empirical table, radar rating or generated figure was changed for this update. Validation checks packaging and references, not search completeness or the truth of literature conclusions.
