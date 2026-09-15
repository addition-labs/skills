# Google Ads audit: six review areas, one pass

Review a Google Ads account from normalized CSV exports; every finding carries its spend and its source fields.

## What it does

Runs six deterministic review areas over reports exported from the Google Ads interface: conversion configuration, search-term spend, brand activity in Shopping and Performance Max, product contribution, repeat buyers, and silent killers. No developer token, no API access, nothing written back to the account.

Each finding is a row with the object, the spend, the conversions and a proposed review action. Nothing is paste-ready: zero recorded conversions is a review signal, and the script writes campaign-scoped negative candidates with a review status, not a negative list. The agent then writes the summary by copying those numbers, never estimating them.

Areas the exports cannot support are marked not measured, never filled with an assumption. Repeat buyers is one of them until verified customer-list data exists, so this pack offers six review areas with unsupported areas marked not measured, not six measured checks.

## Inside

**Conversion configuration review.** Normalizes every action to Primary or Secondary and flags names that suggest a micro-conversion set to Primary or a purchase set to Secondary, for human review. Names do not verify an action's definition; goal usage and custom goals are not measured unless supplied.

**Search terms.** Query rows with cost and zero recorded conversions, plus rows above three times the aggregate CPA of the returned rows (not account CPA). Writes negative_candidates.csv, campaign-scoped, exact match, brand excluded, status "review".

**Brand activity in Shopping and Performance Max.** Query rows matching the brand phrases inside campaigns whose supplied type is Shopping or Performance Max. Attributed cost on reported queries; not incremental sales, not savings.

**Product contribution ranking.** Products ranked by reported conversion value times the supplied margin fraction minus ad cost when margins.csv covers every item; by revenue minus cost otherwise, and the report says which.

**Repeat buyers.** Repeat-buyer spend requires verified customer-list definitions, membership windows, campaign purposes and a report whose audience costs can be aggregated without overlap. The current audience-name export cannot establish it. Reported as not measured until those inputs are available.

**Silent killers.** Campaigns and products with positive cost and zero recorded conversions in the first max(1, floor(rows / 5)) rows by cost, or carrying at least 5% of that report's cost. An Addition screening rule, not a statistical test.

## Needs

Required: conversions.csv, search_terms.csv, campaigns.csv. Optional: products.csv and margins.csv. Export in English and normalize the files to the column names in SKILL.md. Use UTF-8 CSV, one header row, no report-title or date preamble, and no total or subtotal rows. Use a decimal point for numeric values; commas may separate thousands. Do not replace unavailable values with zero. Keep the original exports beside the normalized copies. A missing required column, duplicate header, malformed row or empty required table stops the audit and names the file and row to fix. Brand phrases passed as --brand; account label, currency and export window passed from the intake record. Python 3.10+, no third-party packages.

## Safety

- **Goes to the network:** No. The script reads local CSV files only. The agent's write-up sends the data it reads to the model service configured in your agent.
- **Runs shell commands:** No. One Python script, no subprocesses.
- **Reads secrets:** No. No credentials, no environment variables.
- **Deletes files:** No. Each run requires a new output directory; it never overwrites a previous run.

## Example run

Not run on a live account yet. Version 2.0.0 was run against sixteen synthetic fixtures from the independent release review of 15 September 2026: nine malformed inputs (currency symbol, decimal comma, missing column, localized header, preamble, total row, header-only table, invalid and partial margins) stop with the file and row named; a Performance Max campaign typed only in campaigns.csv is joined correctly (100.00 of brand activity); a product with one conversion and zero value is not called a silent killer; a zero-spend campaign is not flagged; a second run into the same directory is refused. A real run will replace this paragraph.

## Limits

One export window hides seasonality; compare two readings before structural conclusions. Interface exports round currency to two decimals; some queries are withheld for privacy, so visible search-term rows do not reconcile to campaign totals. Google's Recommendations tab is not read or repeated.


_Version 2.0.0 · 2026-09-15 · addition-labs.com · install: `npx skills add addition-labs/skills --skill google-ads-audit`_
