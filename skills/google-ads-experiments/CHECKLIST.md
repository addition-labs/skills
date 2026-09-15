# Checklist: google-ads-experiments

## Before creating the experiment
- [ ] Campaign type and supported experiment type recorded
- [ ] One treatment only
- [ ] Decision metric written: CPA (cost divided by conversions) or ROAS (conversion value divided by cost), not clicks, not CPC
- [ ] Effect size worth acting on written
- [ ] Randomization and reporting unit, allocation and reporting normalization recorded
- [ ] Start date and fixed analysis date set; conversion-lag cutoff written
- [ ] Confidence setting and decision rule written; sample-size rationale written separately (the 50/100 minimums are heuristics)
- [ ] Freeze list written for the base campaign
- [ ] Intended treatment confirmed available for that experiment type; otherwise stop and report

## While it runs
- [ ] No reading before the analysis date
- [ ] No edits to the base campaign (every edit edits the control)
- [ ] External events logged with dates
- [ ] For a bidding or creative test, record and investigate budget constraints. For a budget test, record the planned arm budgets as the treatment and check that the chosen experiment design can identify that change

## Reading
- [ ] Analysis date reached and conversion-lag cutoff passed before exporting both arms: cost, conversions, value, clicks
- [ ] `read_experiment.py` run with the pre-registered metric and --days
- [ ] Descriptive line written as printed; no rounded percentages
- [ ] Scorecard interval for the pre-registered metric quoted at the pre-registered confidence setting
- [ ] Decision is one of: apply, retain control, inconclusive, by the pre-registered rule; no post-hoc extension
