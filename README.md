# Addition skills

Twenty agent skills for SEO, AEO and GEO, paid ads, CRO and content, in the
[Agent Skills](https://agentskills.io) format: one folder per skill, a SKILL.md,
and the reference files the skill loads on demand. They run in Claude Code,
Cursor, Codex, Windsurf and any agent that reads SKILL.md.

Each skill has a page at https://addition-labs.com/skills with the install
command, what it needs, a four-row safety review, the phrases that trigger it,
what is inside, one real run printed in full, and where the method differs.

## Install

```bash
npx skills add addition-labs/skills                            # the whole shelf
npx skills add addition-labs/skills --skill programmatic-seo   # one skill
```

Or copy a folder into `~/.claude/skills/` (every project) or `.claude/skills/`
(this project) and restart the agent.

## The skills

| Shelf | Skill | Install name | What it does | Origin | Licence |
|---|---|---|---|---|---|
| SEO | [Programmatic SEO planner](skills/programmatic-seo/) | `programmatic-seo` | Decides whether a page set should exist, then picks the playbook and template. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| SEO | [Structured data (JSON-LD)](skills/schema/) | `schema` | Adds, fixes or validates schema for ten common page types. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| AEO | [AI search optimisation method](skills/ai-seo/) | `ai-seo` | How ChatGPT, Perplexity, Claude and AI Overviews pick sources, and what to do about it. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| AEO | [AEO and GEO framework](skills/seo-aeo-geo/) | `seo-aeo-geo` | Five layers from extractable structure to entity signals, in order. | [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) @ a67dd34 | MIT |
| AEO | [Five-lane search fix](skills/five-lane-seo/) | `five-lane-seo` | Diagnoses SEO, AEO, GEO, LLMO and Naver with curl, then applies the fixes. | [leopard627/fire-your-seo-agency](https://github.com/leopard627/fire-your-seo-agency) @ eb9be9f | MIT |
| AEO | [Competitive content brief](skills/seo-content-brief/) | `seo-content-brief` | Section-by-section briefs with word counts and scored competitors. | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) @ 55c7914 | MIT |
| Paid ads | [Paid campaign strategy](skills/ads/) | `ads` | Platform choice, account structure and the month-one build for Google, Meta and LinkedIn. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Paid ads | [Ad copy and creative](skills/ad-creative/) | `ad-creative` | Angles, hooks and formats grounded in your winning ads and reviews. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Paid ads | [Attribution models](skills/attribution/) | `attribution` | Which channel caused the sale: seven models, how each lies, and how to reconcile. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Paid ads | [Tracking plan and GA4 setup](skills/analytics/) | `analytics` | Events, GA4, Tag Manager and UTMs, planned before any number is read. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Paid ads | [Reading the ads dashboard](skills/ads-performance-analytics/) | `ads-performance-analytics` | Platform-reported versus real, reconciliation, ROAS versus LTV, incrementality. | [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) @ a67dd34 | MIT |
| CRO | [Page conversion review](skills/cro/) | `cro` | Seven dimensions in impact order, from value proposition to form. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| CRO | [A/B test design](skills/ab-testing/) | `ab-testing` | Hypothesis, sample size, metric tiers and the peeking problem. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| CRO | [Research-first CRO](skills/cro-methodology/) | `cro-methodology` | Conversion Rate Experts’ method: research, objections, then tests. | [wondelai/skills](https://github.com/wondelai/skills) @ c172996 | MIT |
| CRO | [Fix one leaking flow](skills/conversion-optimization/) | `conversion-optimization` | A seven-phase journey: find the leak, research why, change, prove it. | [wondelai/skills](https://github.com/wondelai/skills) @ c172996 | MIT |
| CRO | [Experiment design discipline](skills/experiment-design/) | `experiment-design` | Twelve considerations so a test answers the question you asked. | [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) @ a67dd34 | MIT |
| Content | [Conversion copywriting](skills/copywriting/) | `copywriting` | Headline formulas, hero structure, core sections and CTA copy. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Content | [Seven-sweep copy editing](skills/copy-editing/) | `copy-editing` | Clarity, voice, so-what, proof, specificity, emotion, zero risk. | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ 5b2c000 | MIT |
| Content | [SEO article writer](skills/write-content/) | `write-content` | Research, content-type decision, knowledge extraction, then the draft, with an anti-slop ruleset. | [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) @ 9cf22cc | Apache-2.0 |
| Content | [Pre-publish editorial QA](skills/editorial-qa/) | `editorial-qa` | Brief adherence, fact checks, the AI-content audit and AEO checks before shipping. | [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) @ a67dd34 | MIT |

Five more skills on the site come from the claude-seo plugin and are installed
as that plugin:
- **Full-site SEO audit** (`seo-audit`): calls the claude-seo plugin scripts, so it is installed as that plugin, not copied here. https://addition-labs.com/skills/seo/seo-audit
- **Product-page SEO scoring** (`seo-ecommerce`): calls the claude-seo plugin scripts, so it is installed as that plugin, not copied here. https://addition-labs.com/skills/seo/seo-ecommerce
- **Technical SEO audit** (`seo-technical`): calls the claude-seo plugin scripts, so it is installed as that plugin, not copied here. https://addition-labs.com/skills/seo/seo-technical
- **GEO page analysis** (`seo-geo`): calls the claude-seo plugin scripts, so it is installed as that plugin, not copied here. https://addition-labs.com/skills/aeo/seo-geo
- **Content quality and E-E-A-T score** (`seo-content`): calls the claude-seo plugin scripts, so it is installed as that plugin, not copied here. https://addition-labs.com/skills/content/seo-content

## Origin and licences

Every folder is a verbatim copy of its upstream folder at the commit named in
its `NOTICE.md`, with the upstream `LICENSE` beside it. The authors are named
in the table above. One folder (`five-lane-seo`) carries a one-line change,
recorded in its NOTICE: the frontmatter `name` matches the folder, as the
specification requires.

The skills contain no scripts, no executables and no credentials: markdown,
JSON and text files, a licence and a notice per folder. What a skill can do to
your machine is what the agent running it can do; the safety review on each page
at addition-labs.com says which skills read the web and which edit files.

## Updating

Upstream repositories move. A skill here is pinned to the commit in its NOTICE;
when the shelf is refreshed, the commit changes and the NOTICE with it.
