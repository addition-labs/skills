# Checklist: google-ads-audit

## Before the run
- [ ] Intake recorded: account label, currency, export window start and end, brand phrases (including misspellings and the retailer's own name if it differs)
- [ ] Required files exported for that window: conversions.csv, search_terms.csv, campaigns.csv; optional products.csv and margins.csv
- [ ] Files normalized: English column names from SKILL.md, one header row, no preamble, no total or subtotal rows, decimal point, no currency symbols, no blank required cells
- [ ] `conversions.csv` carries Action optimization (Primary/Secondary) or the legacy Include in "Conversions" Yes/No column
- [ ] Every campaign named in search_terms.csv is present in campaigns.csv with its type
- [ ] `margins.csv`, if supplied, covers every item in products.csv with a fraction from 0 to 1
- [ ] Original exports kept beside the normalized copies
- [ ] Output directory for this run does not exist yet
- [ ] Python 3.10+, no packages to install

## After the run
- [ ] `findings.json`, `negative_candidates.csv`, `change_list.md`, `manifest.json` all exist in the run directory
- [ ] manifest.json shows the intended account, currency and window
- [ ] Every `not_measured` line in findings.json appears in the write-up, never filled
- [ ] Each review action names one object, one spend figure and the proposed review, with its source fields
- [ ] Brand and non-brand reported on separate lines and labelled as the returned query rows only
- [ ] Headline says "contribution" only when margins were supplied for every product; otherwise "revenue after ad spend"
- [ ] Areas not summed as independent waste

## Before changing anything in the account
- [ ] Review list read by the person who owns the account
- [ ] Negative candidates reviewed for intent, measurement and conversion lag; no negatives is a valid result
- [ ] Approved negatives added as exact match, in the campaign the row names, from an upload file built only from approved rows
- [ ] Any conversion-action change agreed first, with its goal usage checked; it changes what every later report means
- [ ] Brand coverage changed only after an incrementality test
- [ ] Note the run directory; the next review compares against it
