# Can short vertical video be called the fastest-growing medium by consumption time?

Assessment date: **9 November 2026**.

**Finding:** growth can be estimated, but the selected evidence does not establish first place across media by consumption time. Recent platform disclosures support continued growth in video consumption. A provisional comparison of survey snapshots suggests a much smaller increase in short-video time than popular view-count comparisons imply.

## What the existing project establishes

The [2026 snapshot](../data/media_use_2026.md) gives short video 88.5% weekly reach, 426 weekly minutes and 4.26 days per week. It leads the available labeled media proxies on reach and frequency; games have slightly more weekly time, at 433 minutes. Missing observations and broader music consumption prevent an all-art ranking. Failure to establish universal leadership is not evidence that short video definitely loses it.

The financial table has only one short-video landmark, an annualized Reels revenue pace in 2025. Its derivative cannot be estimated. Revenue growth would measure monetization as well as consumption. Subjective radar scores have no measured historical trajectory.

## A provisional numerical comparison

The July 2025 DataReportal article reports 6 hours 42 minutes for short video, 4 hours 57 minutes for long online video, and 10 hours 15 minutes for all TV per week. The current project retains the later short/long values; the Digital 2027 article also reports all-TV time of 9 hours 58 minutes.

| Source category | July 2025 report: weekly minutes | Q2 2026 observation: weekly minutes | Difference | Relative difference |
| --- | --- | --- | --- | --- |
| Short online video | 402 | 426 | +24 | +5.97% |
| Long online video | 297 | 299 | +2 | +0.67% |
| All TV, including streaming | 615 | 598 | -17 | -2.76% |

Sources: [Digital 2025 July](https://datareportal.com/reports/digital-2025-july-global-statshot), [Digital 2027](https://datareportal.com/reports/digital-2027-global-overview-report), and the [retained snapshot](../data/media_use_2026.md).

**These are conditional arithmetic differences, not validated population growth estimates or year-on-year rates.** The earlier article warns of expanded coverage of people aged 65+. The later report excludes Russia and describes revised media-time questions. Exact earlier chart footnotes, matching country/age coverage, weights and question wording were not independently resolved in this extension. Publication dates must not substitute for fieldwork dates. Sampling uncertainty was not available for these differences.

If the observations can be harmonized, short video would have grown faster than these two video aggregates over this interval. This would still leave music, games, books and other art forms unranked. All TV also overlaps the project's film/series categories.

## Recent platform evidence and its limits

In its **Q3 2026 call**, Meta reports double-digit year-on-year growth in Facebook Reels time spent globally and in the US. Instagram total time per user also grew double digits, but includes Feed. The reported Instagram Reels recommendation uplift of over 4% is a different measure; it is not an annual growth rate. [Original transcript, printed pages 5–6](https://s21.q4cdn.com/399680738/files/content_files/META-Q3-2026-Earnings-Call-Transcript.pdf).

Facebook announced in June 2025 that all new videos would become Reels, with no length or format restrictions. Therefore this product's growth cannot isolate short vertical video, and category expansion may affect the comparison. [Facebook format change](https://about.fb.com/news/2025/06/making-it-easier-create-videos-facebook/).

YouTube changed Shorts views on 31 March 2025 to count starts and replays without a minimum watch time. Do not interpret a comparison of the old 70-billion and new 200-billion daily-view milestones as measured consumption growth. Prefer watch time or consistently defined engaged views. [YouTube revision history](https://developers.google.com/youtube/reporting/revision_history?hl=en).

## How to estimate the derivative

Choose one outcome and one population. For consumption, use weekly minutes per person across a fixed population, including nonusers, or total person-hours. Do not multiply an all-person time average by reach again.

For observations separated by `dt` years:

```text
absolute growth = (M1 - M0) / dt
annualized relative growth = (M1 / M0) ** (1 / dt) - 1
```

The first gives added weekly minutes per person per elapsed year; the second gives a compound annualized percentage. They can produce different leaders. Audience reach requires a separate calculation in percentage points per year. Shares of a common media-time budget can test whether a format gains attention relative to the other measured forms, provided overlap is handled consistently.

Two harmonized waves estimate an interval-average slope. To discuss acceleration, obtain at least three waves; for a claim about growth now, prioritize recent matched quarters rather than a launch-to-present average. Several waves help separate seasonality, noise and structural changes. A fixed country/age panel of repeated cross-sections would suffice; tracking the same people is not required.

For artistic consumption specifically, estimate the artistic fraction `a(t)` of format time `M(t)`. Then artistic exposure is `a(t) * M(t)`; growth in the overall format does not identify growth in that artistic subset when `a(t)` changes. A clear coding definition and sampled content audit are needed.

## Wording supported by this extension

Use: **Short video combines very broad reach with evidence of continued consumption growth.**

The growth questions are centralized as H04–H05 in [Project hypotheses](../research/06_hypotheses.md), with answers and confidence in [Findings](01_findings.md#answers-to-the-project-hypotheses). Establishing a growth leader requires a specified interval, geography, metric and comparison set, harmonized series, and an assessment of measurement uncertainty. A largest observed estimate in an incomplete set does not establish a universal winner.

This extension adds no interpolated history, harmonized growth ranking, or changes to the radar scores. The provisional table is not an input to the figure generator.
