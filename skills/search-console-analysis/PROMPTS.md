# Prompts: search-console-analysis

## 1. Setup check

```
Use the search-console-analysis skill. Confirm the OAuth client file exists at <absolute path> and that
the dependencies listed in Setup are installed in the virtual environment. Tell me the exact property
string to use for <example.com> (sc-domain or URL-prefix) and why. Do not pull yet.
```

## 2. Pull

```
Run the installed scripts/gsc_pull.py with the virtual environment's Python: --site "<sc-domain:example.com>",
--client-secret "<absolute path>", --out "<absolute runs directory>". Report the run directory it printed,
the row counts per file from manifest.json, the date windows, and whether the run is marked complete.
If it reports an incomplete run, show the error and the recovery action and stop. Do not analyse yet.
```

## 3. Analyse and write

```
Run scripts/gsc_analyze.py --dir "<exact run directory from the pull>" --brand-terms "<brand,brandstore>".
Read findings.json and write the summary in the template from SKILL.md: WHAT HAPPENED · WHAT IT MEANS ·
WHAT TO DO (at most seven, one page and one number each) · NOT MEASURED (every item from findings.json).
Say "averaged position", never "ranks #N". Call the unit query-page candidates. If the striking-distance
list is all brand terms, say that first. Do not score CTR gaps; the skill does not measure them.
```

## 4. One list, deeper

```
Take the highest-impression non-brand query-page candidates from striking_distance. Use an available
browser to inspect the current result pages for <country>, <language> and <device>, and inspect our
matching page and potential source pages. Save source URLs and observation dates. If browsing or page
content is unavailable, list those checks as not measured. Do not infer competitor headings, missing
sections or usable internal links from Search Console metrics alone.
```

## 5. Lost impressions, honestly

```
Take lost_impressions and lost_impressions_unknown. Record overlapping updates from Google's official
Search Status Dashboard and separately list documented site changes for the windows in findings.json.
An overlap is context, not attribution. For each page, without evidence identifying a cause, report the
cause as unknown. Pages in the unknown list need a page-filtered request before any claim.
```
