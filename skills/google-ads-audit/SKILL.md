---
name: google-ads-audit
description: >-
  Review Google Ads conversion setup, search-term spend, brand traffic and
  product performance from local CSV exports. Use when the user requests an
  account audit or asks which queries, campaigns or products need investigation.
  Validate export schemas and reporting scope, run the local audit, and return
  evidence with campaign-scoped review candidates. Requires conversion-action,
  search-term and campaign exports; product, margin and audience data support
  additional checks. Does not retrieve or modify a Google Ads account.
metadata:
  version: 2.0.0
  released: 2026-09-15
  author: addition-labs.com
---

# Google Ads audit: six review areas, one pass

The script reads normalized CSV exports, validates them, and writes evidence. It proposes nothing paste-ready: every
line in its output is a review candidate with the spend behind it, and areas it cannot support are marked not measured.

## Input contract

Export in English and normalize the files to the column names below. Use UTF-8 CSV, one header row, no report-title or
date preamble, and no total or subtotal rows. Use a decimal point for numeric values; commas may separate thousands. No
currency symbols. Do not replace unavailable values with zero. Keep the original exports beside the normalized copies. A
missing required column, duplicate header, malformed row, total row or empty required table stops the audit and names the
file and row to fix. Nothing is guessed.

| file | required | columns (exact names; listed aliases are normalized explicitly) |
|---|---|---|
| `conversions.csv` | yes | Conversion action · Action optimization (`Primary` or `Secondary`; the legacy `Include in "Conversions"` Yes/No column is accepted and mapped) · Conversions · Conv. value |
| `search_terms.csv` | yes | Search term · Campaign · Cost · Conversions · Conv. value · optional Match type |
| `campaigns.csv` | yes | Campaign · Campaign type · Cost · Conversions · Conv. value. Every campaign named in search_terms.csv must appear here |
| `products.csv` | no | Item ID · Title · Cost · Conversions · Conv. value, one row per item |
| `margins.csv` | no | Item ID · Margin as a fraction from 0 to 1, one row for every item in products.csv |

Audience-name exports are not read: audience names alone do not enable the repeat-buyer calculation (see area 5).

## Run

Locate `scripts/audit.py` relative to this SKILL.md. Use an absolute script path and explicit input and output directories.
Use a fresh output directory for every account and run; an existing output directory is an error. Account label, currency
and the export window come from the intake record, never from a guess about when the script ran.

```bash
python3 "/absolute/path/to/installed/google-ads-audit/scripts/audit.py" \
  --input "/absolute/path/to/account/input" \
  --out "/absolute/path/to/account/runs/run-name" \
  --brand "acme,acme store" --currency GBP \
  --account "Acme UK" --window-start 2026-08-16 --window-end 2026-09-14
```

Outputs: `findings.json` (every finding row, no display slices), `negative_candidates.csv` (campaign-scoped, brand
excluded, status "review"), `change_list.md` (review candidates in plain prose) and `manifest.json` (account, window,
currency, file row counts, version).

## The six review areas

1. **Conversion configuration review.** Normalizes each action to Primary or Secondary. Flags names that suggest a
   micro-conversion set to Primary, or a purchase set to Secondary, for human review; names do not verify the action's
   definition. Campaign goal usage, custom-goal membership, conversion definitions and configured call duration are
   reported as not measured unless supplied. Do not change an action's optimization setting from its name alone.
2. **Search terms.** Query rows with positive cost and zero recorded conversions, and positive-conversion rows whose CPA
   is greater than three times the aggregate CPA of the returned search-term rows. That aggregate is not account CPA.
   Hidden search terms, campaign types and conversion-goal differences limit the comparison; the multiplier is an
   Addition screening rule. Zero recorded conversions is a review signal, not a negative: check the query against your
   products, business goal and conversion lag before approving it. Create an upload file only from approved rows,
   retaining the campaign and exact-match setting. The brand/non-brand split covers the returned query rows only.
3. **Brand activity in Shopping and Performance Max.** Query rows matching the brand phrases (whole words) inside
   campaigns whose supplied type is Shopping or Performance Max. This is attributed cost on reported queries. It does not
   measure incremental sales, organic substitution or savings from exclusions. Review campaign roles and run an
   incrementality test before changing brand coverage.
4. **Product contribution ranking.** Contribution means reported conversion value multiplied by the supplied margin
   fraction, minus reported ad cost. Confirm the value is revenue on the same tax, refund and currency basis as the
   margin. If any product lacks a margin, supply it or rerun without the margin file so the entire ranking uses revenue
   after ad spend. This is not verified accounting profit.
5. **Repeat buyers.** Not measured. Repeat-buyer spend requires verified customer-list definitions, membership windows,
   campaign purposes and a report whose audience costs can be aggregated without overlap. An audience-name export cannot
   establish it.
6. **Silent killers.** Campaigns and products with positive cost and zero recorded conversions when they are in the first
   `max(1, floor(number of rows / 5))` rows sorted by descending cost, or carry at least 5% of that report's cost. An
   Addition screening rule, not a statistical test. Keywords are not checked. Report the date window and conversion lag
   before proposing a pause.

## Write-up rules for the agent

- Copy numbers from `findings.json`; every summary there names its source fields. If an area is `not_measured`, say so in
  one line; do not fill it.
- The six areas overlap: the same spend can appear in several lists. Never sum them as independent waste.
- Some queries are withheld for privacy, so visible search-term rows do not necessarily reconcile to campaign totals.
- Say "contribution" only when margins were supplied for every product; otherwise "revenue after ad spend".
- No recommendation from Google's own Recommendations tab is used or repeated here.

## Safety

The Python script reads local CSVs and makes no network calls. It reads no credentials and launches no subprocesses. It
creates a new output directory per run and refuses an existing one. The agent's write-up sends the data it reads to the
model service configured in your agent. No Google Ads account changes are made by this script.

## Limits

- One export window hides seasonality; compare two readings before drawing structural conclusions, and say "two readings",
  not "a trend".
- Interface exports round currency to two decimals.
- This reviews. It does not push changes to the account.
