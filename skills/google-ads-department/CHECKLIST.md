# Checklist: google-ads-department

## Intake
- [ ] Account, currency, timezone, objective, margin and value definitions recorded
- [ ] Campaign types, budget ceiling, primary actions and campaign goals recorded; unknowns left unknown
- [ ] Measured conversion lag recorded from evidence, never defaulted
- [ ] Restricted settings and the accountable reviewer named
- [ ] plan.md and changes.csv started in the account directory with today's date

## Before proposing a change
- [ ] Setting compared with plan.md and the campaign type's supported options
- [ ] Bidding choice supported by the campaign type and current Google eligibility, source and date recorded; unsupported or undocumented choices returned as blocked
- [ ] Brand treatment matches the documented campaign role and available incrementality evidence
- [ ] Proposed negatives reviewed for intent, scope, measurement and conversion lag; no negatives is a valid result
- [ ] Row appended to changes.csv with reason, evidence, approver and rollback condition

## Weekly
- [ ] Change log read before judging outcomes
- [ ] Outcome review waits for the measured conversion-lag window and the experiment plan. Record urgent repairs separately with their reason; do not apply a universal waiting period
- [ ] Report written with windows and source files named; brand and non-brand split only where supported
- [ ] Open experiments checked against their pre-registration (google-ads-experiments)

## Monthly
- [ ] Audit package run (google-ads-audit) into a new run directory
- [ ] changes.csv reviewed: every change has a date, a reason, evidence and a status
- [ ] Handover current: each protected setting listed with its reason and its actual review date or condition
