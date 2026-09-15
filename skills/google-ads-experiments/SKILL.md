---
name: google-ads-experiments
description: >-
  Plan and review a Google Ads experiment for a specific campaign type and
  business decision. Use when the user wants to test a bidding, budget or
  creative change, or interpret a completed experiment. Define the treatment,
  metric, allocation, analysis date and decision rule; summarize CPA or ROAS
  from validated arm totals and use the chosen metric's reported uncertainty.
  Aggregate totals alone cannot establish significance. Produces a plan or
  review; does not create or apply an account experiment.
metadata:
  version: 2.0.0
  released: 2026-09-15
  author: addition-labs.com
---

# Google Ads experiments: plan first, then read, in that order

## Before you create the experiment (the pre-registration record)

Record the campaign type and supported experiment type; the single treatment; the business decision metric; the effect
size worth acting on; the randomization and reporting unit; traffic or budget allocation; start date; fixed analysis
date; conversion-lag cutoff; confidence setting and decision rule; and the settings that must remain unchanged. Record
the sample-size rationale separately. The historical 50/100-conversion rules are Addition screening heuristics, not
power calculations, Google requirements or proof of significance. A low-volume result is inconclusive unless the
pre-registered rule says otherwise.

- **One treatment.** Budget, or bidding target, or creative, or match type. Not two.
- **Decision metric.** Cost divided by conversions (CPA), or conversion value divided by cost (ROAS). Not clicks, not CPC.
- **Fixed analysis date**, set before launch, after at least two full weekly cycles plus the conversion-lag cutoff.
- **Allocation and experiment type**, recorded as Google shows them, with the reporting normalization.
- **Freeze list.** Every setting on the base campaign that will not be touched during the test.

## Setting it up in Google Ads

Open Campaigns, then Experiments, then create an experiment using the type supported for the selected campaign. Record
the campaign and experiment type, eligible treatment settings, split type and reporting normalization before creating
it. If the intended budget or bidding treatment is not available for that type, stop and report that limitation. Do not
substitute a different experiment without changing the plan. Use the Experiments page directly; do not use Google's
Recommendations tab.

## While it runs

- Do not read the result before the analysis date. A "winner" on day four is a coin flip with a chart.
- Do not edit the base campaign. Every edit is an edit to the control.
- Log external events with dates: promo, stockout, price change, Google update. Concurrent randomization helps both arms
  experience the same external conditions. An even split does not guarantee balance, and an unequal split does not by
  itself create seasonal bias. Record allocation, experiment type, conversion lag and any reporting normalization before
  comparing arms.

## Reading it (analysis date, after the conversion-lag cutoff)

Export both arms: cost, conversions, conversion value, optionally clicks. Then:

```bash
python3 "/absolute/path/to/installed/google-ads-experiments/scripts/read_experiment.py" \
  --control 4200,63,5100,3000 --trial 4150,81,5900,3100 --metric cpa --days 28
```

The helper calculates observed CPA or ROAS and relative difference. It does not test significance. For a decision, use
the experiment's reported interval for the pre-registered metric and confidence setting, together with the planned
decision rule and completed conversion-lag window. If the required interval or suitable underlying data is unavailable,
report a descriptive comparison and no statistical decision. Google's experiment scorecard reports metric-specific
confidence; preserve its selected setting rather than replacing it with a different threshold. The checklist controls
when to analyze; the helper does not verify the experiment's history. Commas delimit the arm fields, so thousands
separators are not accepted.

## Sentences you are allowed to write

- The helper's line: "Trial CPA X vs control Y over N days, with A and B conversions (Z%). Descriptive comparison only."
- "Apply / retain control / inconclusive, by the pre-registered rule, using the scorecard interval for <metric> at
  <confidence>."

## Sentences you are not allowed to write

- "The test is already showing" (before the analysis date)
- "Roughly a 20% improvement" (rounded; use the number)
- "Significant" from arm totals alone, or anything about a metric that was not the pre-registered decision metric
- An extension decided after inspecting results, unless the pre-registered design specifies that procedure

## Safety

The helper reads command-line numbers only: no network, no files, no credentials, no subprocesses. It creates or
applies nothing in the account.
