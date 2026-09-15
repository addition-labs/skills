# Search Console analysis: more rows than the interface export

Retrieve more Search Console rows than the interface export and compare two date windows, with every limit named.

## What it does

The interface export stops at a thousand rows. The API exposes more. This skill retrieves query x page x device rows and page-only rows for a current window and the previous window of the same length, 25,000 rows per request until no further rows are returned for that request, and writes them as CSVs with a manifest that records property, search type, dimensions, filters, reporting timezone, date windows, row counts and completion status.

Pagination collects the rows the API exposes; it does not recover anonymized queries or guarantee a complete query table. Query-row totals can differ from property totals because of query omissions and aggregation differences.

Two deterministic analyses run on a completed run directory: striking-distance query-page candidates (inclusive averaged position 5 through 15, at least 500 impressions, CTR of at least 1%, compared unrounded) and page impression losses (page-only tables, at least 500 previous impressions, an unrounded decline of at least 20%; a page absent from the current result is unknown, not zero). CTR gaps against a benchmark curve are not measured: no verified curve ships with the skill. The agent writes the summary in three parts and lists everything the data could not answer as not measured.

## Inside

**Pull.** gsc_pull.py authenticates once with your own Google account (OAuth desktop flow), caches the token at a path you control, pages through the API and writes a new run directory with current.csv, previous.csv, current_pages.csv, previous_pages.csv and manifest.json. A failed request leaves the run marked incomplete; the analyzer refuses it.

**Striking distance.** Query-page candidates averaging position 5 through 15 with real impressions and clicks. Review whether the existing page meets the query's intent before choosing a revision, another page or no change. Averaged position is a candidate, not a rank.

**Lost impressions.** Pages present in both page-only tables, down 20% or more unrounded against the previous window, ranked by absolute loss. Overlapping Google updates are context, not attribution.

**CTR gap.** Not measured by default. CTR comparisons need a named, dated curve with its market, device, query scope and source values. A site-specific comparison is preferable when the data supports it. A CTR gap is a review candidate, not proof that a title or description caused lost clicks. No comparison is scored when the curve is unavailable.

**Brand flag.** Queries containing your brand phrases (whole words) are flagged, not removed. If every striking-distance candidate is a brand term, the report says so first.

## Needs

A Google Cloud project with the Search Console API enabled, a configured OAuth consent screen and a Desktop OAuth client file saved at a path you pass to the puller; an account with access to the exact property; the property string (sc-domain: or URL-prefix); a virtual environment with google-api-python-client and google-auth-oauthlib. The analyzer needs only the standard library.

## Safety

- **Goes to the network:** Yes. The puller uses Google's OAuth authorization and token services and the Search Console API (read-only scope); first consent opens a browser and a temporary local callback server. The analyzer makes no network calls. The agent's write-up uses the model service configured in your agent.
- **Runs shell commands:** No. You run Python commands; neither script contains a shell-command runner.
- **Reads secrets:** Yes. The OAuth client file and the cached token, at paths you pass; keep their contents out of prompts and reports.
- **Deletes files:** No. The puller writes a new run directory per pull and creates or updates the token file; the analyzer overwrites only findings.json in the directory you name.

## Example run

Not run on a live property yet. Version 2.0.0 was exercised on 15 September 2026 with a fake API service (pagination over 25,007 rows, page-only pulls, a refused second run into the same directory, a quota failure leaving an incomplete manifest that the analyzer refused) and on a synthetic table where an averaged position of 15.04 is excluded unrounded, a 19.995% decline is not called a 20% loss, a 499-impression page is excluded, and a page absent from the current result is reported as unknown. A real run on one of our properties will replace this paragraph.

## Limits

Google documents a maximum of 50,000 rows per day per search type and does not guarantee all rows; two whole-window calls do not implement the daily retrieval pattern. History is 16 months. Positions are averages across devices. The skill reads; it writes nothing to Search Console or your site.


_Version 2.0.0 · 2026-09-15 · addition-labs.com · install: `npx skills add addition-labs/skills --skill search-console-analysis`_
