# Checklist: search-console-analysis

## Setup (once)
- [ ] Google Cloud project with Search Console API enabled; OAuth consent screen configured; Desktop OAuth client created
- [ ] If the app is in testing, the consenting account is added as a test user
- [ ] Client file saved at a path you control; its contents never pasted into chat
- [ ] Virtual environment created and the dependencies from Setup installed in it
- [ ] Property string decided: `sc-domain:` for the whole domain, URL-prefix for a single host

## Before the pull
- [ ] The consenting Google account has access to the exact property
- [ ] Windows understood: current window and the previous window of the same length; Pacific reporting date, default lag 3 days
- [ ] `--out` root chosen; the run directory under it does not exist yet

## After the pull
- [ ] The puller printed the run directory and manifest.json says complete
- [ ] Row counts per file noted; the run ended on "no further rows returned for this request", not on an auth or quota error
- [ ] Valid schema and pull completion verified; an empty table is reported as no rows returned
- [ ] An incomplete run is kept as incomplete and not analysed

## After the analysis
- [ ] `findings.json` written into the exact run directory you named
- [ ] Both lists present even if empty; empty is a finding; unknown pages listed separately from losses
- [ ] Brand queries flagged, not removed; non-brand reported first
- [ ] Every position written as "averaged position"; the unit called query-page candidates
- [ ] Each action names one page and one number
- [ ] NOT MEASURED carries every item from findings.json, including CTR gap
- [ ] Search Status Dashboard overlap and site changes recorded as context, cause reported as unknown unless evidenced
