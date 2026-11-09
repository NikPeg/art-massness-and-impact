# Social breadth and active participation: selected recent surveys

Added 9 November 2026. These observations extend the meaning of mass participation beyond audience reach, time, and frequency. They are not 2026 observations or new radar scores. Source IDs resolve in the [source register](../sources/source_register.md).

## Survey bases

| source | survey | fieldwork | geography | population | final_sample_n |
| --- | --- | --- | --- | --- | --- |
| PS24T | Participation Survey 2023/24, technical context | May 2023-March 2024 | England | Adults aged 16+ | 171748 |
| PS25T | Participation Survey 2024/25 | April 2024-March 2025 | England | Adults aged 16+ | 34378 |
| EB25 | Special Eurobarometer 562 | 18 February-16 March 2025 | EU27 | Resident EU citizens aged 15+ under the survey nationality rules | 26319 |

The England figures are final achieved samples, not target sample sizes or bases for every subgroup. Random address selection, web/paper modes, weighting, and quality checks are documented. The 2024/25 individual response rate was 24%; large samples do not remove nonresponse bias. Some questions use online-only random modules. The 2023/24 sample is retained as methodological context, not as a second observation for the results below. Sources: PS24T, PS25T.

## England: social and territorial breadth

Unit: weighted percentage within each listed group. Fieldwork: 2024/25; recall: preceding 12 months, collectively extending from April 2023 to March 2025. Physical arts engagement includes attendance and personal activities such as reading; it is not venue attendance alone. Digital engagement uses the survey's selected arts activities. Source: PS25, section 2, Figures 2.14-2.15 and Annex 3.

| source | measure | group | participation_percent |
| --- | --- | --- | --- |
| PS25 | Physical arts engagement | Most deprived areas, IMD decile 1 | 81 |
| PS25 | Physical arts engagement | Least deprived areas, IMD decile 10 | 95 |
| PS25 | Digital arts engagement | Most deprived areas, IMD decile 1 | 31 |
| PS25 | Digital arts engagement | Least deprived areas, IMD decile 10 | 39 |
| PS25 | Physical arts engagement | West Midlands, ITL2 area | 85 |
| PS25 | Physical arts engagement | North Yorkshire, ITL2 area | 95 |

These are broad arts aggregates, not observations for each of the eight categories. Area deprivation is not personal income. ITL2 West Midlands is a different geographic unit from the identically named ITL1 region. The report identifies the deprivation contrasts as statistically significant; no new significance tests or uncertainty estimates were calculated here.

## EU27: active artistic participation

Unit: weighted percentage of the surveyed population reporting an activity within the preceding 12 months. Source: EB25, question QA3, report pages 43-44 (PDF pages 43-44, zero-based 42-43). Multiple responses; do not add rows. The total also covers activities not individually selected below.

| source | activity | participation_percent |
| --- | --- | --- |
| EB25 | Any listed artistic activity | 49 |
| EB25 | Singing | 15 |
| EB25 | Playing a musical instrument | 11 |
| EB25 | Making films or doing photography | 10 |
| EB25 | Writing poems, essays, novels, etc. | 5 |

Film and photography form a combined source category. Writing includes essays. These cannot be assigned to isolated film, book, or video-format audiences. Singing and instrument-playing overlap. This is creation/performance, not consumption, recognition, or attributable life change.

## Reuse

Retain survey populations, periods, and categories. Do not compare the England and EU totals as identical measures, fill missing GWI cells, or infer an eight-form global winner. [The participation generator](../scripts/build_participation_figures.py) reads these tables to produce [EU activities](../figures/active-participation-eu-2025.svg) and [England social breadth](../figures/social-breadth-england-2024-25.svg), each with an adjacent TXT annotation. The two regional observations and survey-base table supply context and are not plotted.

## Pictures and digital creation: Australia, report 2026

Source: PICCREATE26, Australian Survey of Social Attitudes, 985 responses used from five survey waves. The report describes overall fieldwork spanning late 2024 to January 2026, with minor date inconsistencies between its overview and appendix; these are not calendar-year 2026 population estimates. Sample drawn from registered adult voters in Australia, not all global internet users.

| source | main_content_type | share_of_creators_percent |
| --- | --- | --- |
| PICCREATE26 | Photography | 20 |
| PICCREATE26 | Video | 19 |
| PICCREATE26 | Writing | 13 |
| PICCREATE26 | Visual art and craft | 9 |
| PICCREATE26 | Memes | 1 |

The main-type question is asked of respondents reporting digital creation during the preceding 12 months. The total report sample is not this question's denominator. These are rounded main-type shares, not the proportion of all adults making each type. Do not sum selected rows into picture participation: visual art/craft includes other work and secondary activities are not measured. The questionnaire excludes everyday family/friend documentation for social purposes. The official HTML shorthand says “respondents”; the PDF's main-type wording and conditional denominator take precedence. Source bases and totals contain inconsistencies, so no population share is derived.

The existing EB25 film/photography observation remains combined; it cannot supply a separate pictures rate. These new observations are not added to the EU chart or the common GWI snapshot because their questions, populations, and denominators differ.
