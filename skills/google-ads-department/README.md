# Google Ads planning and review, as a workflow

A Google Ads planning and review workflow for one operator: intake, change review, weekly report, handover.

## What it does

Use it to record account goals, review proposed changes against the plan and the evidence, prepare a weekly report and hand over open work. It does not schedule recurring work, spawn agents, build campaigns or push changes. The audit and experiment helpers are separate packages (google-ads-audit, google-ads-experiments).

The point is not automation. It is that the same questions are asked on every account before a change is made, and that a proposal whose settings contradict the plan or lack evidence is returned as blocked, with the missing evidence named, instead of being applied.

## Inside

**Intake.** Account, currency, timezone, business objective, margin and value definitions, campaign types, budget ceiling, primary actions, campaign goals, measured conversion lag, restricted settings and the accountable reviewer. Unknown values stay unknown.

**Working files.** plan.md, changes.csv, experiments.md and report.md in a directory you choose; created when absent, updated without erasing history.

**Bidding strategy.** Chosen per campaign type, objective, measurement and eligibility, with the source and date recorded. Addition's cold-start sequence for Search and Shopping campaigns is stated as our operating rule, scoped to those campaign types, not as a Google requirement.

**Change review.** Each proposal compared with the plan, campaign-type support, measurement, budget ceiling and conversion-lag evidence; returned as ready for owner review, blocked, or revised with the exact corrected proposal.

**Weekly review and handover.** Change log read first; brand and non-brand separated only where the data supports it; windows and source files named; every open item with owner, evidence needed and next review condition.

## Needs

An account directory you choose, the intake answers, and exports or reports you supply as evidence. No connection to the account. Nothing to install beyond the skill.

## Safety

- **Goes to the network:** No.
- **Runs shell commands:** No.
- **Reads secrets:** No.
- **Deletes files:** No. It writes the four working files in the directory you choose and never erases history.

## Example run

Packaged workflow not yet validated end to end. Before release, run the included intake, change review and handover against an explicitly labelled synthetic account brief or an approved redacted account. Preserve the brief, exact request, plan, proposed change, review decision and handover. A script is not required for this demonstration.

## Limits

Written for e-commerce accounts with a product feed; lead-generation accounts skip feed and Shopping questions. A prose weekly cadence is not a scheduler; a review record is not an enforced push gate. The workflow reviews; the account owner applies.


_Version 2.0.0 · 2026-09-15 · addition-labs.com · install: `npx skills add addition-labs/skills --skill google-ads-department`_
