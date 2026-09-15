---
name: search-console-analysis
description: >-
  Analyze Google Search Console performance for a named property and explicit
  comparison windows. Use when the user requests query opportunities, CTR
  investigation or a search-traffic decline review. Read compatible exports or
  retrieve data through the included read-only OAuth script after setup.
  Validate scope and completeness, then report supported findings and missing
  evidence. CTR comparisons require a declared baseline; page-loss claims
  require comparable page-level data. Does not edit the site.
metadata:
  version: 2.0.0
  released: 2026-09-15
  author: addition-labs.com
---

# Search Console analysis: more rows than the interface export, two windows, named limits

## What this does

1. `scripts/gsc_pull.py` authenticates with YOUR Google account (OAuth, one-time browser consent) and retrieves, for
   the current window and the previous window of the same length, query x page x device rows AND page-only rows,
   25,000 rows per request until no further rows are returned for that request. It writes a new run directory with
   four CSVs and a manifest (property, search type, filters, dimensions, reporting timezone, date windows, row counts,
   completion status). Pagination collects the rows the API exposes; it does not recover anonymized queries or
   guarantee a complete query table.
2. `scripts/gsc_analyze.py` reads one completed run directory and writes `findings.json` with:
   - **striking_distance**: query-page candidates with inclusive averaged position 5 through 15, at least 500
     impressions and CTR of at least 1%, compared unrounded. Review whether the existing page meets the query's intent
     before choosing a revision, another page or no change.
   - **lost_impressions**: pages present in both page-only tables with at least 500 impressions in the previous window
     and an unrounded decline of at least 20%. A page absent from the current page result is listed as unknown, never
     as a 100% loss.
   - **ctr_gap**: not measured by default. No verified comparison curve ships with this skill.
   These are configurable Addition screening rules, not Google requirements or evidence of causal improvement.
3. You (the agent) read `findings.json` and write the plain-language summary using the template below. Numbers are
   copied, never rounded up, never estimated.

## Setup (once)

Create a Google Cloud project, enable Search Console API, configure its OAuth consent screen and audience, and create a
Desktop OAuth client. If the app is in testing, add the consenting account as a test user. That account must have access
to the exact Search Console property. Save the downloaded client file at the path supplied to the puller; do not paste
its contents into chat. Create a virtual environment, install the listed dependencies there, and run the puller with that
environment's Python. Setup duration is not measured.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install google-api-python-client google-auth-oauthlib
```

## Run

```bash
.venv/bin/python "/absolute/path/to/installed/search-console-analysis/scripts/gsc_pull.py" \
  --site "sc-domain:example.com" \
  --client-secret "/absolute/path/to/config/client_secret.json" \
  --out "/absolute/path/to/gsc-runs"            # optional: --days 28 --lag 3 or --end YYYY-MM-DD

python3 "/absolute/path/to/installed/search-console-analysis/scripts/gsc_analyze.py" \
  --dir "/exact/directory/printed/by/the/pull" --brand-terms "example,examplestore"
```

The puller prints the run directory; pass exactly that directory to the analyzer. The analyzer never selects a
directory on its own, so it cannot pick another property's results. Brand queries are flagged (whole words), not removed.

Operational contract: every pull writes to a new directory. A run is complete only after all CSVs and the manifest have
been written successfully. The manifest records exact property, dates, dimensions, filters, search type, row counts and
completion status. Analysis requires that completion record. On authentication or quota failure the puller reports the
affected request and recovery action, retains the incomplete run as incomplete, and the analyzer refuses it. Dates use
Search Console's Pacific reporting date; the default lag of 3 days allows for finalization. An empty table is reported as
no rows returned, not as an error; an absent file is an error.

## Reading rules (binding for the write-up)

- Average position is an average. A query at "position 6" can be #2 on mobile and #12 on desktop. Say "averaged
  position", never "ranks #6".
- The unit is query-page candidates, not queries. Say so.
- If every striking-distance candidate is a brand term, say so first: the non-brand list is the real opportunity.
- Query-row totals can differ from property totals because of query omissions and aggregation differences.
- Record overlapping updates from Google's official Search Status Dashboard and separately list documented site changes.
  An overlap is context, not attribution. Without evidence identifying a cause, report the cause as unknown.
- CTR comparisons need a named, dated curve with its market, device, query scope and source values. A site-specific
  comparison is preferable when the data supports it. A CTR gap is a review candidate, not proof that a title or
  description caused lost clicks. No comparison is scored when the curve is unavailable. `--legacy-ctr-curve` exposes an
  unvalidated legacy configuration for research only; its output is labelled as such and is not a benchmark.
- Zero rows is a result, not an error: "no candidate met the thresholds" is a valid finding.

## Write-up template

```
WHAT HAPPENED: <n> query-page candidates within striking distance, <n> pages lost impressions
  (<current window> vs <previous window>, property <name>).
WHAT IT MEANS: one sentence per list, plain language, the biggest number in bold.
WHAT TO DO: at most seven actions, each tied to one page and one number, lowest effort first.
NOT MEASURED: every item from findings.json not_measured (conversions, AI Overview presence, CTR gap, ...).
```

## Safety

**Network:** The puller uses Google's OAuth authorization and token services and the Search Console API. First consent
opens a browser and a temporary local callback server. The analyzer makes no network calls. The agent's write-up uses the
model service configured in your agent.

**Commands:** You run Python commands. The puller opens the consent browser; neither script contains a shell-command runner.

**Credentials:** The puller reads the OAuth client file at the path you pass and creates or updates the token file beside
it (or at `--token`). Its requested Search Console scope is read-only. Keep credential contents out of prompts and reports.

**Files:** The puller writes CSVs and manifest.json into a new run directory under `--out` and creates or updates the token
file. The analyzer writes findings.json in the directory selected by `--dir` and overwrites a previous findings.json there.
Neither script calls a delete API or changes the website or Search Console property.

## Limits, stated

- Google documents a maximum of 50,000 rows per day per search type and does not guarantee that all rows are returned;
  page/query grouping can drop data. Two whole-window calls do not implement Google's daily retrieval pattern. For larger
  properties, pull daily with consistent dimensions and aggregate clicks and impressions by sum and position by
  impression weighting; the completeness warning still applies.
- The API returns at most 16 months of history.
- This skill reads. It does not write to Search Console and it does not touch your site.
