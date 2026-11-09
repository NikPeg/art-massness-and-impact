# Reproduction and validation record

## Participation figures, 9 November 2026

Added the standalone participation generator and validator. The full build now produces 16 SVGs and the gallery, including both participation charts and their TXT annotations. Ran the standalone build/check and the complete build/check successfully. The new validator checks displayed percentages against Markdown inputs, 0-100% tick scales, label coordinates, and sidecar presence. Both SVGs were visually inspected in a browser through a temporary loopback server; labels, markers, and full scales were visible without overlap or clipping. The server was stopped after inspection.

## Participation extension check

On 9 November 2026, after adding the two selected survey programmes, `python3 scripts/validate.py` passed. It checks local links and English text in the new Markdown file as part of the package; it does not validate the new numerical observations. Those were manually checked against the DCMS main/technical reports and Eurobarometer QA3 and methodology. No figures were regenerated, because their inputs did not change.

Date: 9 November 2026.

Commands run from the project root:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

Results:

```text
Generated 13 SVG figures and figures/index.html
PASS: 40 financial cells; 5 US years; 8 snapshot rows; 80 scores and rationales; 13 SVGs; local links; English text.
```

Earlier project validation included browser inspection of the original seven-category gallery and chat radars. For this eight-category extension, the generator and validator were rerun successfully. Snapshot height and axis/footer positions now depend on row count so the eighth row remains inside the SVG. A new browser visual inspection was not completed: the browser policy blocked local file URLs. XML parsing and structural checks do not establish pixel-level layout quality, verify source producers' data, or validate subjective judgments. Scripts contain no network dependencies.

The project is a reproducible exploratory dossier, not a validated causal ranking of artistic media.
