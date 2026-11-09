# Methods and reproduction

## Scope and comparison units

The project is an exploratory dossier on eight categories of internet-distributed creative content: short-form video, long-form horizontal creator video, music, feature films, series, books and video games, and pictures. These categories overlap; they are not exclusive shares of a common market or attention budget. Definitions and inclusion rules are in [scope and measurement](01_scope_and_metrics.md).

Keep reach, consumption time, frequency, commercial scale, cultural recognition and life influence distinct. Life influence has two separately reported outcome families: major events and everyday/cumulative changes. Within everyday outcomes, distinguish immediate responses, repeated responses, during-exposure trajectories and persistence after exposure changes or ends. No common cross-medium life-impact index is estimated.

For comparisons of influence, distinguish equal attentive time, complete works and repeated practices over a common period. Creator relationships and community participation are separate exposure units. A single clip is not equivalent to years of participation in a community. The [proposed primary study](../results/03_next_study.md) specifies measurements needed for these comparisons; that study has not been conducted.

## Evidence selection and literature-review procedure

The literature component is an exploratory evidence map with a moderate, documented targeted search. Public original reports, company disclosures, research papers and methodologically described syntheses supply evidence. Record observation date, population, geography, unit, reporting vintage and retrieval level. Study findings are classified by exposure, comparator, design, outcome, follow-up and applicability to the question.

The [documented search](../sources/moderate_review_search_2026.md) records eight exact web queries, search date, selection rules, candidate decisions and access limits on 9 November 2026. The corpus also includes targeted searches recorded in the [research log](../sources/research_log.md), including the [everyday/cumulative appraisal](08_cumulative_media_effects.md). The eight-query record covers its specified search, not every source in the dossier. Documentation and appraisal depth vary across the corpus; no retrospective uniform protocol or complete screening record is claimed.

This bounded search procedure is repeatable, but web rankings may change and a complete export of returned hits is unavailable. There was no systematic database search, exhaustive citation chasing, independent screening or formal study-level risk-of-bias assessment. Original full-text, abstract-only and discovery-only sources remain distinguishable in the [source register](../sources/source_register.md). No effect-direction filter is used for the documented search. Missing or unretrieved evidence is not evidence of no effect.

## Confidence in conclusions and search coverage

Confidence attaches to the exact claim and population, not to a medium as a whole. Consider design quality and causal identification, directness of exposure/comparator/outcome/follow-up, consistency across relevant evidence, and precision where checked. High/Moderate/Low labels are informal reasoned assessments, not scores, calibrated probabilities or a completed standardized certainty framework. High confidence in a reported survey observation does not imply high confidence in a broad causal comparison.

Use Not assigned when no comparable body supports the requested conclusion. Abstract-only evidence is provisional, with unverified details stated; a causal conclusion cannot be upgraded from an abstract alone. Report search coverage separately, including languages, retrieval failures and unsearched databases. A non-significant result does not establish a negligible effect without considering precision. Studies sharing participants, and reviews containing the same primary studies, are not independent replications.

## Empirical inputs and transformations

Markdown tables in `data/` are the authoritative script inputs. `NA` means missing, not zero. Incompatible populations and reporting vintages remain separate; no five-year series is interpolated or inferred from platform totals.

| Input | Treatment | Boundary |
| --- | --- | --- |
| [2026 media use](../data/media_use_2026.md) | Convert reported weekly hours/minutes to weekly minutes, then divide by seven for a daily mean; frequency stays days per week | International online-adult survey proxies do not consistently isolate artistic content or the project's categories |
| [Annual context](../data/annual_indicators.md) | Store annual dollars in billions; sum the two AAP fiction categories; multiply reported BLS hours by 60 for the US time-use figure | Market totals, company revenue, box office and annualized revenue pace are incompatible; financial values appear in tables without a common chart |
| [Participation](../data/participation_and_breadth.md) | Preserve published activity categories, recall periods, denominators and achieved sample sizes | England and EU surveys describe different populations and activities; no harmonization, microdata analysis or extrapolation to 2026 is performed |

Whole-market revenues, print-inclusive publishing, cinema attendance, broad listening and US diaries are contextual evidence, not matched online-only observations. Missing online-only measures remain gaps. Consumer participation, original creation, remixing and redistribution are distinct activities.

## Category-specific measurement

**Long horizontal video.** The working category requires landscape orientation, at least ten minutes and authored creative treatment, with alternative duration thresholds proposed for sensitivity checks. Feature films and scripted series have separate primary categories. GWI long online video is a broader reach/time/frequency proxy that does not verify these inclusion rules. All five financial observations for this category are missing. Creator attachment, genre and duration are not causally separated by the available aggregate observations.

**Pictures.** Online photography, illustration, drawings, collages and image memes follow the scope rules. No matched picture-only observation supplies reach, time, frequency or revenue for the common tables. Empirical values remain missing; all six radar data markers are qualitative. Gallery experience, memory, news attention and creator-only main-type shares answer different questions and do not calibrate the radar.

**Music.** The main profile covers direct listening and audible music embedded in online short/long video, films, series and games. Combined reach, time and days require within-music unions, not summed platform audiences. The [music scenario table](../data/music_online_scenarios.md) provides a streaming-only reference, drawn as a dashed segment on the first three radar axes. This is a difference in exposure definition, not a measured uplift. The literature does not causally isolate musical contributions from the host audiovisual work.

**Participation.** Special Eurobarometer 562 and England's Participation Survey supply the two participation figures. Percentage axes run from 0 to 100. England's connectors compare deprivation groups, not change over time or uncertainty. An earlier survey wave supplies sample-size context only; repeated cross-sections do not measure individual retention.

## Subjective radar profiles

All eight profiles have the same six axes in order: reach, time, frequency, money, cultural recognition and general Life impact. Each axis has a subjective 0–10 author score, giving 48 scores and 48 rationale entries. The [score table](../data/subjective_scores_2026.md) and [rationales](../data/score_rationales.md) define the current inputs. Profiles are closed and lightly filled; the overview and gallery follow alphabetical English category names, without area ranking or a composite total.

The radius is linear on the author scale. No normalization against observed consumption or revenue, calibrated evidence-to-score formula, independent assessor procedure or empirical validation of the point differences is claimed. A filled circle means a numerical source informed a judgment; a hollow diamond means qualitative reasoning only. Both remain subjective scores. The general Life impact score represents author interpretation of potential lasting influence on an engaged person, not a measured effect or an established comparative ordering. It is not an average of detailed research outcomes. The illustrative profiles are separate from the literature-based findings.

## Figure generation and reproduction

Run from the project root with Python 3.9 or newer:

```sh
python3 scripts/build_figures.py
python3 scripts/validate.py
```

The standard-library generator reads local tables and writes 15 standalone SVGs, adjacent TXT annotations and `figures/index.html`: eight individual radars, one eight-panel overview, four consumption-context figures and two participation figures. No network request, external chart library or empirical re-estimation occurs during the build. Figures and gallery are in English; the radar reading guide is Russian TXT. The [script notes](../scripts/README.md) describe output and marker conventions.

## Validation and maintenance

The validator checks input categories and counts, selected numerical anchors, missing values, score bounds, rationale coverage, music-scenario consistency, SVG structure, overview panels, accessibility IDs, label bounds, participation percentages and scales, TXT consistency, local file links and figure language. The [validation record](../results/04_validation.md) states current checks and limits. These checks establish packaging and internal consistency, not pixel-perfect layout, source accuracy, search completeness or scientific validity of author judgments.

For an empirical input change, update its table, source and method note, rebuild affected outputs and validate. For an author score change, update its rationale and audit as well. Do not fill a missing empirical observation with an opinion. The [further-work plan](../FURTHER_WORK.md) specifies the protocol, comprehensive search, independent appraisal and synthesis required for a full systematic review.

Historical implementation notes are kept in [the method archive](../sources/method_history.md) and [research log](../sources/research_log.md), separately from this description of the current methods.
