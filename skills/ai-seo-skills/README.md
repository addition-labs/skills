# Sixteen SEO playbooks, one installable skill

One installable skill with sixteen SEO playbooks. The playbooks contain instructions, not bundled scripts.

## What it does

Install `ai-seo-skills` once; the agent reads the root SKILL.md, selects the playbook matching the job you asked for, and follows only that folder's instructions. Keyword and prompt research, citation gap, cannibalisation check, internal link builder, title and meta rewrite, schema generator, crawl audit, Search Console pull, rank tracking, answer-block rewrite, entity corpus, semantic gap, refresh queue, backlink opportunities, GEO visibility audit, index recovery.

Each playbook declares its inputs, a job-specific procedure, its output artifact and the work it could not perform. Search Console API retrieval depends on the separately installed search-console-analysis skill. Other playbooks use supplied evidence and any explicitly available read tools.

## Inside

**Research.** Keyword and prompt research; entity corpus; semantic gap against a competitor page.

**Rankings.** Search Console pull (through the separate skill); rank tracking across dated snapshots; cannibalisation check.

**Pages.** Title and meta rewrite with character counts; answer-block rewrite with a claim/source table; schema generator with eligibility notes; crawl audit from an export with an explicit schema.

**Links.** Internal link builder from link edges plus an independent URL inventory; backlink opportunity review from separate exports.

**AI search.** Citation gap from actual engine answers; GEO visibility audit with a per-function crawler access matrix.

**Recovery.** Refresh queue from comparable performance periods; index recovery from URL-level status and crawl evidence.

## Needs

Your own exports and evidence: Search Console tables, a crawl export, backlink exports, page copies, a fixed prompt list, engine transcripts. Where a playbook needs a browser, fetch tool or engine connection it says so and reports the check as not measured when the tool is unavailable.

## Safety

These playbooks contain instructions, not bundled executable scripts. File-based checks use the supplied evidence. Live SERP inspection, citation measurement, competitor-page comparison and crawl-access tests require an available browser, fetch tool or engine connection and therefore make network requests. Name the actual tool and destination before using it. An unavailable connection produces a not-measured result. Credentials belong to the connected tool or the separate Search Console skill, never to the report. Outputs are drafts and local evidence files; these playbooks do not publish changes, send messages or modify the site.

- **Goes to the network:** Only when a playbook names a tool and destination for live inspection.
- **Runs shell commands:** No.
- **Reads secrets:** No. OAuth files belong to the separate search-console-analysis skill.
- **Deletes files:** No.

## Example run

Not run as a packaged set. Version 2.0.0 replaced the earlier four-step generic body with a job-specific procedure per playbook after the independent review of 15 September 2026. Per-playbook example runs on an explicitly labelled synthetic or approved redacted dataset will be added before each one is cited as validated.

## Limits

No scripts are bundled. Thresholds and screens are Addition's own and are stated inside each playbook; adjust them to your traffic scale and say so. Reuse a recorded procedure and its evidence table on the next run.


_Version 2.0.0 · 2026-09-15 · addition-labs.com · install: `npx skills add addition-labs/skills --skill ai-seo-skills`_
