# Prompts: google-ads-audit

Copy one block at a time. Replace the angle-bracket parts. Nothing else needs editing.

## 1. Intake (before exporting anything)

```
Use the google-ads-audit skill. Before I export, tell me exactly which reports you need from the
Google Ads interface, the columns each file must contain after normalization, and the export rules
(English, one header row, no preamble, no total rows, decimal point, no currency symbols). Record the
intake: account label <name>, currency <GBP>, export window <YYYY-MM-DD> to <YYYY-MM-DD>, brand phrases
<brand, brand store>. Do not start the audit yet.
```

## 2. Run

```
The normalized exports are in <absolute input directory> (conversions.csv, search_terms.csv,
campaigns.csv<, products.csv, margins.csv>). Run the installed scripts/audit.py by absolute path with
--input, a fresh --out directory <absolute path/runs/YYYY-MM-DD-account>, --brand "<phrases>",
--currency <XXX>, --account "<label>", --window-start and --window-end from the intake. If the script
stops with a schema error, show me the file and row it names and wait; do not edit the data yourself.
Then read findings.json and write the summary. Copy every number; if an area says not_measured, say so
in one line and move on.
```

## 3. Write-up in the house format

```
Write the review for <who reads it: the owner / the media buyer>. Three parts:
WHAT HAPPENED (numbers from findings.json with their source fields, biggest in bold) · WHAT IT MEANS
(one plain sentence per finding) · WHAT TO REVIEW (at most seven review actions from
findings.json review_actions, each with the object, the spend and the proposed action, lowest effort
first). End with NOT MEASURED. Report brand and non-brand for the returned query rows only and say so.
Do not sum the areas as independent waste. Do not quote Google's Recommendations tab.
```

## 4. The negative candidates

```
Open negative_candidates.csv from the run directory. Group the rows by intent (competitor · job seeker ·
DIY · unrelated product · brand of a retailer). For each row keep the campaign. Flag any term that could
also be a real buyer, and note that zero recorded conversions inside the window may be conversion lag.
I approve rows by hand; build an upload file only from the rows I approve, exact match, in the campaign
the row names.
```

## 5. Second pass, a quarter later

```
Compare findings.json from <earlier run directory> with findings.json from <today's run directory>.
Both manifests must show the same account and currency; say so. List what closed, what reopened, and
what is new. Same three-part format. Do not claim a trend from two points; say "two readings".
```
