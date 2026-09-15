# Prompts: google-ads-experiments

## 1. Pre-registration (the only prompt that matters)

```
Use the google-ads-experiments skill. I want to test <raising the budget 30% / tROAS 350 to 300 /
a new creative> on campaign <name>, campaign type <Search / Shopping / Performance Max / ...>.
Write the pre-registration record with me: campaign and experiment type, single treatment, decision
metric (CPA or ROAS), effect size worth acting on, randomization and reporting unit, allocation,
start date, fixed analysis date, conversion-lag cutoff, confidence setting and decision rule, freeze
list, and the sample-size rationale as a separate line. Push back if I try to test two things. The
base campaign did <N> conversions in the last 28 days; say whether the analysis date is realistic at
that rate, and say that the minimums are heuristics, not power calculations.
```

## 2. Setup check before launch

```
Here is the experiment setup I entered in Google Ads: <paste the settings, including experiment type,
split type and reporting normalization>. Compare it line by line with the pre-registration. List every
difference. If the intended treatment is not available for this experiment type, say so and stop. Do
not say "looks fine" if anything differs.
```

## 3. While it runs (when tempted)

```
It is day <N> of <analysis date>. I am not asking for a result. Log this external event with its date:
<promo / stockout / price change / Google update>. Remind me what the freeze list says.
```

## 4. Reading it

```
Analysis date reached and the conversion-lag cutoff has passed. Control: cost <>, conversions <>, value
<>, clicks <>. Trial: cost <>, conversions <>, value <>, clicks <>. Run scripts/read_experiment.py with
--metric <cpa|roas> --days <N>. Write the descriptive line it prints, then the scorecard's reported
interval for the pre-registered metric at the pre-registered confidence setting.
```

## 5. The decision

```
Compare the completed experiment against the pre-registered decision rule using its chosen metric and
uncertainty interval. Return apply, retain control, or inconclusive, with the evidence. Do not extend
after inspecting results unless the pre-registered design specifies that procedure. A new test requires
a new plan.
```
