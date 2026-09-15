#!/usr/bin/env python3
"""Deterministic analyses over one completed pull directory (v2.0.0, 2026-09-15). No network, no estimates.

Reads current.csv / previous.csv (query x page x device) and, when present, current_pages.csv / previous_pages.csv
(page only). Writes findings.json into the same directory. Values are compared unrounded; rounding happens only
when a selected row is written out.
"""
import argparse, csv, json, math, re
from pathlib import Path

VERSION = "2.0.0"
STRIKE = dict(pos_min=5.0, pos_max=15.0, impr_min=500, ctr_min=0.01)   # inclusive averaged position 5 to 15
LOSS = dict(prev_impr_min=500, min_decline_pct=20.0)
RULES_NOTE = "configurable Addition screening rules, not Google requirements or evidence of causal improvement"
# Unvalidated legacy configuration, opt-in only (--legacy-ctr-curve). Values are Addition assumptions with no
# verified source; a scored CTR gap is a review candidate, never proof that a title or description lost clicks.
LEGACY_CURVE = {1: .2766, 2: .1559, 3: .1003, 4: .0691, 5: .0435, 6: .0337, 7: .0257, 8: .0210, 9: .0186, 10: .0163}
LEGACY_TAIL, LEGACY_FACTOR = .012, 0.6
FIELDS = ["clicks", "impressions", "ctr", "position"]


class DataError(Exception):
    pass


def load(path, dims):
    if not path.is_file():
        raise DataError(f"missing file {path.name}")
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        need = dims + FIELDS
        missing = [c for c in need if c not in (reader.fieldnames or [])]
        if missing:
            raise DataError(f"{path.name}: missing column(s) {missing}")
        rows = []
        for i, r in enumerate(reader, start=2):
            try:
                vals = {k: float(r[k]) for k in FIELDS}
            except (TypeError, ValueError):
                raise DataError(f"{path.name} row {i}: non-numeric metric")
            if any(not math.isfinite(v) or v < 0 for v in vals.values()):
                raise DataError(f"{path.name} row {i}: negative or non-finite metric")
            rows.append({**{d: r[d] for d in dims}, **vals})
    return rows


def agg_query_page(rows):
    acc = {}
    for r in rows:
        a = acc.setdefault((r["query"], r["page"]), dict(query=r["query"], page=r["page"], clicks=0.0, impressions=0.0, pos_w=0.0))
        a["clicks"] += r["clicks"]; a["impressions"] += r["impressions"]; a["pos_w"] += r["position"] * r["impressions"]
    out = []
    for a in acc.values():
        if a["impressions"] == 0:
            continue
        a["position"] = a["pos_w"] / a["impressions"]
        a["ctr"] = a["clicks"] / a["impressions"]
        del a["pos_w"]; out.append(a)
    return out


def fmt(r, **extra):
    o = dict(r); o["position"] = round(o["position"], 2); o["ctr"] = round(o["ctr"], 4)
    o["clicks"] = int(o["clicks"]) if float(o["clicks"]).is_integer() else o["clicks"]
    o["impressions"] = int(o["impressions"]) if float(o["impressions"]).is_integer() else o["impressions"]
    o.update(extra); return o


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", type=Path, required=True, help="exact completed pull directory printed by gsc_pull.py")
    ap.add_argument("--brand-terms", default="", help="comma-separated brand phrases; matching queries are FLAGGED (whole words), not removed")
    ap.add_argument("--legacy-ctr-curve", action="store_true", help="opt in to the unvalidated legacy CTR curve (research only)")
    a = ap.parse_args()
    d = a.dir.expanduser().resolve()
    required = ["current.csv", "previous.csv", "manifest.json"]
    missing = [n for n in required if not (d / n).is_file()]
    if missing:
        ap.error(f"incomplete pull directory {d}: missing {', '.join(missing)}")
    manifest = json.loads((d / "manifest.json").read_text())
    if not manifest.get("completed"):
        ap.error(f"pull directory {d} is not marked complete (status {manifest.get('status')!r}); do not analyze an incomplete run")
    try:
        cur, prev = load(d / "current.csv", ["query", "page", "device"]), load(d / "previous.csv", ["query", "page", "device"])
        pages_ok = (d / "current_pages.csv").is_file() and (d / "previous_pages.csv").is_file()
        pc_rows, pp_rows = (load(d / "current_pages.csv", ["page"]), load(d / "previous_pages.csv", ["page"])) if pages_ok else ([], [])
    except DataError as e:
        ap.error(str(e))
    brand = [b.strip() for b in a.brand_terms.split(",") if b.strip()]
    pats = [re.compile(r"(?<!\w)" + re.escape(b) + r"(?!\w)", re.I) for b in brand]
    is_brand = lambda q: any(p.search(q) for p in pats)
    warn, not_measured = [], ["conversions", "AI Overview / AI Mode presence", "per-device split (aggregated here)"]
    if not cur:
        warn.append("current.csv has no rows: no query-page-device rows were returned for the current window.")
    if not brand:
        warn.append("No --brand-terms given: brand queries are not flagged.")

    qp = agg_query_page(cur)
    striking = [fmt(r, is_brand=is_brand(r["query"])) for r in qp
                if STRIKE["pos_min"] <= r["position"] <= STRIKE["pos_max"] and r["impressions"] >= STRIKE["impr_min"] and r["ctr"] >= STRIKE["ctr_min"]]
    striking.sort(key=lambda r: -r["impressions"])
    if striking and all(r["is_brand"] for r in striking):
        warn.append("Every striking-distance candidate is a brand term; the non-brand list is the real opportunity.")

    ctr_gap = []
    if a.legacy_ctr_curve:
        for r in qp:
            if r["impressions"] < STRIKE["impr_min"]:
                continue
            p = int(round(r["position"]))
            bench = LEGACY_CURVE.get(p, LEGACY_TAIL if p <= 15 else None)
            if bench and r["ctr"] < LEGACY_FACTOR * bench:
                ctr_gap.append(fmt(r, benchmark_ctr=bench, ctr_gap=round(bench - r["ctr"], 4), is_brand=is_brand(r["query"])))
        ctr_gap.sort(key=lambda r: -(r["ctr_gap"] * r["impressions"]))
        warn.append("CTR-gap list uses the UNVALIDATED LEGACY CURVE (Addition assumptions: curve values, 0.6 factor, 1.2% tail). Research only; not an objective benchmark.")
    else:
        warn.append("CTR-gap scoring is not measured: no verified comparison curve was supplied. Review query, device, brand and search-result context before proposing titles.")
        not_measured.append("CTR gap against a benchmark curve")

    lost, unknown = [], []
    if pages_ok:
        pc = {r["page"]: r["impressions"] for r in pc_rows}; pp = {r["page"]: r["impressions"] for r in pp_rows}
        for page, before in pp.items():
            if before < LOSS["prev_impr_min"]:
                continue
            if page not in pc:
                unknown.append(dict(page=page, impressions_prev=int(before), note="absent from the current page result; run a page-filtered request before assigning zero"))
                continue
            now = pc[page]; pct = 100 * (now - before) / before
            if pct <= -LOSS["min_decline_pct"]:
                lost.append(dict(page=page, impressions_prev=int(before), impressions_now=int(now), change_pct=round(pct, 1), lost=int(before - now)))
        lost.sort(key=lambda r: -r["lost"])
        if unknown:
            warn.append(f"{len(unknown)} page(s) with previous impressions are absent from the current page result; their comparison is unknown, not zero.")
    else:
        warn.append("Page impression losses are not measured: page-only tables (current_pages.csv, previous_pages.csv) are absent. Supply comparable page-level measurements.")
        not_measured.append("page impression losses")

    findings = dict(version=VERSION, property=manifest.get("property"), search_type=manifest.get("search_type"),
                    windows=manifest.get("windows"), reporting_timezone=manifest.get("reporting_timezone"),
                    rows_current=len(cur), rows_previous=len(prev), query_page_candidates_current=len(qp),
                    thresholds=dict(striking_distance=STRIKE, page_loss=LOSS, note=RULES_NOTE),
                    unit="query-page candidates", striking_distance=striking, ctr_gap=ctr_gap,
                    lost_impressions=lost, lost_impressions_unknown=unknown, warnings=warn, not_measured=not_measured,
                    source_files=["current.csv", "previous.csv"] + (["current_pages.csv", "previous_pages.csv"] if pages_ok else []))
    (d / "findings.json").write_text(json.dumps(findings, indent=2, allow_nan=False))
    print(f"striking {len(striking)} · ctr_gap {len(ctr_gap)} · lost_impressions {len(lost)} (unknown {len(unknown)}) · rows {len(cur)} → {d/'findings.json'}")


if __name__ == "__main__":
    main()
