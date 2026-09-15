# Prompts: ai-seo-skills

One prompt per group. Name the playbook; the agent reads the root SKILL.md, then only that playbook's SKILL.md.

## Research

```
Use ai-seo-skills, playbook keyword-prompt-research. Seed terms: <topic list>. Search Console export:
<path> with query, page, clicks, impressions, position and window. Give me observed queries and
proposed prompt ideas as separate labelled rows, each with intent and classification, with the
supporting URL or passage and observation date for any content gap. No invented volumes.
```

## Rankings

```
Use ai-seo-skills, playbook search-console-pull, then cannibalisation-check on the result. Property:
<sc-domain:example.com>. Flag concurrent query-page overlaps that meet the impression screen; assess
switching only if date-level history was supplied. For each pair: query, both URLs, evidence,
classification (harmful overlap, distinct intent, unresolved) and proposed action.
```

## Pages

```
Use ai-seo-skills, playbook title-meta-rewrite on <export path>. Use the supplied review-candidate
list, if present; report its source. For each row: URL, old and new title, old and new description,
rationale and character counts. Treat character limits as editorial constraints, not Google display
guarantees. Keep brand suffix rules as they are.
```

## Links

```
Use ai-seo-skills, playbook internal-link-builder. Link edges: <export path>. URL inventory:
<sitemap or CMS export>. Join the supplied page traffic and candidate files by URL; if either is
missing, use only link evidence and label priority unmeasured. Propose at most three links per source,
each with the anchor, the real placement passage from the source page, and the evidence.
```

## AI search

```
Use ai-seo-skills, playbook citation-gap. Fixed prompts: <list or file>. Engines: <names>, using
<supplied transcripts / the available engine connection>. Target domain: <ours>. Competitors: <list>.
Report completed and failed observations separately; count a gap only where a completed answer cites a
competitor and not us. Then playbook geo-visibility-audit on the pages that lost citations: access
matrix by crawler function from robots rules and documented tokens, with simulated fetches labelled
as simulations.
```

## Recovery

```
Use ai-seo-skills, playbook refresh-queue on the measured page-level comparison <path, windows>. If
only two windows exist, report only that comparison and mark 90-day decay unavailable. Then playbook
index-recovery on any URL with an excluded or unindexed status in the supplied Search Console evidence.
Queue: URL, measured change, source window, stale passage or indexing cause, proposed change, recheck
condition. Unresolved causes stay unresolved.
```

## Every playbook, the write-up

```
Summarize observations, interpretation and proposed action. Use numbers only when supplied or
calculated from recorded inputs. End with unavailable evidence and its effect on the result.
```
