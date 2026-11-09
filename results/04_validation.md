# Reproduction and validation record

## Current eight-category package, 9 November 2026

The target scope is creative content distributed through the internet. The full build produces 15 SVGs and the HTML gallery: eight individual radar profiles, one radar overview, four consumption context figures, and two participation figures. The data contain 40 financial cells, eight snapshot rows, and 40 subjective numeric scores, eight unassessed Life impact entries, and 48 corresponding rationale entries. Radar consumption and money judgments have now been revised for online-only use; contextual empirical observations retain their original scopes. Music includes substantive embedded online musical contact, with a separately labeled streaming-only reference.

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
