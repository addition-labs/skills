# Changelog: search-console-analysis

## 2.0.0 (2026-09-15)
- Completeness wording: pagination collects the rows the API exposes; Google's row limits cited (G1).
- Page-level losses use separate page-only pulls; absent pages are unknown, not zero (G2).
- Analyzer requires --dir and a manifest marked complete; no implicit newest-directory selection (G3).
- CTR-gap scoring not measured by default; legacy curve opt-in and labelled unvalidated (G4).
- Unrounded comparisons; previous-window minimum documented (G5).
- Setup with venv and consent screen; argument checks; Pacific reporting date; incomplete runs kept and refused (G6).
- Safety text names OAuth traffic, the local callback and the token file path; credentials at user-controlled paths (G7).
- Deeper-read prompts require observed evidence; unit is query-page candidates; update overlap is context (G8).

## 1.0 (2026-09-15)
- First packaged version.
