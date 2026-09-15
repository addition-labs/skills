# Google Ads experiments without fooling yourself

Pre-register the test, then read it: one treatment, one metric, a fixed analysis date, a decision rule written before launch.

## What it does

Google Ads can split-test a budget, a bidding target or a creative change against a copy of the campaign, with different experiment families for different campaign types. The tool is right; the reading mistakes are old. This skill fixes the decisions before launch and keeps the reading descriptive until the pre-registered rule and the scorecard's own interval say otherwise.

Before the experiment: campaign and experiment type, one treatment, the decision metric (CPA or ROAS), the effect size worth acting on, allocation, start date, fixed analysis date, conversion-lag cutoff, confidence setting and decision rule, and a freeze list for the base campaign. During: no peeking, no edits, external events logged with dates.

After: a small helper takes cost, conversions and value per arm, prints per-arm CPA or ROAS and the relative difference, and states that aggregate totals do not provide an uncertainty estimate. The decision comes from the pre-registered rule and the experiment's reported interval, not from the helper.

## Inside

**Pre-registration.** The record written before the experiment exists, and the checklist says why each line matters. The historical 50 and 100 conversion minimums are Addition screening heuristics, not power calculations or proof of significance.

**Setup.** Which Experiments page path to use, what to record about type, allocation and reporting normalization, and when to stop because the intended treatment is not available for that campaign type.

**Reading helper.** read_experiment.py with --control and --trial as cost,conversions,value[,clicks], --metric and --days. Validates the arms (finite, non-negative, cost above zero, three or four fields) and prints a descriptive line. Fractional conversions are printed as supplied.

**Allowed sentences.** The descriptive line, and a decision phrased against the pre-registered rule and the scorecard interval.

**Forbidden sentences.** "Already showing", rounded percentages, "significant" from totals alone, and any metric that was not pre-registered.

## Needs

Export of both arms after the analysis date and conversion-lag cutoff: cost, conversions, conversion value, optionally clicks; the experiment scorecard's reported interval for the pre-registered metric. Python 3.10+, standard library only.

## Safety

- **Goes to the network:** No.
- **Runs shell commands:** No.
- **Reads secrets:** No.
- **Deletes files:** No. The helper writes nothing.

## Example run

```
python3 scripts/read_experiment.py --control 4200,63,5100,3000 --trial 4150,81,5900,3100 --metric cpa --days 28
Trial CPA 51.23 vs control 66.67 over 28 days, with 81 and 63 conversions (-23.1%). Descriptive comparison only. These aggregate totals do not provide a valid uncertainty estimate for CPA. No apply decision is supported by this calculation alone.
```

Version 2.0.0 was also checked on 15 September 2026 against the independent review's failure cases: a missing field, a fifth field, a zero cost, a negative duration and a zero-conversion arm each stop with a named error; 50.4 and 50.6 conversions print as supplied. No live experiment has been read with this version yet.

## Limits

The helper describes; it does not test. Fractional conversion credit, conversion lag and campaign-type differences all live in the scorecard's interval, not in arm totals. The skill plans and reviews; it creates and applies nothing in the account.


_Version 2.0.0 · 2026-09-15 · addition-labs.com · install: `npx skills add addition-labs/skills --skill google-ads-experiments`_
