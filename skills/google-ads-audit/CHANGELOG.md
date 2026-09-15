# Changelog: google-ads-audit

## 2.0.0 (2026-09-15)
- Strict input contract: normalized English CSV, header validation, explicit aliases, no blank or guessed values, total rows and preambles rejected, every file validated before any output exists (A1).
- Zero-conversion queries become campaign-scoped review candidates (negative_candidates.csv); nothing paste-ready; brand excluded consistently (A2).
- Conversion configuration review reads a normalized Action optimization column; names flag for review only; goal usage and definitions reported as not measured (A3).
- Brand activity in Shopping and Performance Max uses the supplied campaign type from campaigns.csv, whole-word brand phrases, and no savings claim (A4).
- Product contribution requires a complete margin file or falls back to revenue after ad spend for every row; duplicate items rejected (A5).
- Repeat buyers reported as not measured; audience names are not read (A6).
- Silent killers test zero conversions (not zero value), positive cost, exact integer rule; keywords not checked (A7).
- findings.json carries every row, source fields, brand/non-brand of returned rows, review actions and manifest; no truncation (A8).
- --input, --out (fresh directory), --account, --window-start/--window-end from the intake record (A9).

## 1.0.1 (2026-09-15)
- PURCHASE regex word-bounded; product silent-killer rule applied to all products.

## 1.0 (2026-09-15)
- First packaged version.
