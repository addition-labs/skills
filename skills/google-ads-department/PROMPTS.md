# Prompts: google-ads-department

## 1. Intake (new account or new quarter)

```
Use the google-ads-department skill. Run the intake with me, one question at a time: account,
currency, timezone, business objective, margin and value definitions, campaign types, budget ceiling,
primary conversion actions, campaign goals, measured conversion lag, restricted settings, accountable
reviewer. Leave unknown values unknown. Write plan.md in <account directory> from the answers, with
the evidence dates. For each campaign, state which bidding strategies its type supports and what
eligibility evidence is still missing; do not assign a strategy from a conversion count alone.
```

## 2. Review a proposed change

```
Proposed change for campaign <name>: <exact setting, old value, new value, reason>. Compare it with
plan.md, the campaign type's supported settings, the measurement configuration, the budget ceiling and
the conversion-lag evidence in changes.csv. Return one of: ready for owner review, blocked (name the
missing evidence), or revise (give the exact corrected proposal). Append the row to changes.csv with
status. Do not say it has been applied.
```

## 3. Weekly report

```
Write this week's report.md: observations first with the numbers as exported, nothing rounded; brand
and non-brand on separate lines only where the exports support the split; one paragraph per change in
changes.csv and what the data shows after it, marking anything younger than the measured conversion
lag as not yet judged; proposed actions with their evidence; not measured. Name the windows and source
files. Source: <paste the exports or name the files>. Do not use the Recommendations tab.
```

## 4. Experiment register

```
Update experiments.md: for each open experiment, the pre-registration record, status, evidence to date
and unresolved decisions. Use the google-ads-experiments skill for the pre-registration format. Do not
read a result before its analysis date.
```

## 5. Handover

```
Write the handover for account <name>: plan.md summary, changes.csv since <date>, open experiments,
and for each open item the owner, the evidence needed and the next review condition. List each
protected setting, the reason it is protected and its actual review date or condition.
```
