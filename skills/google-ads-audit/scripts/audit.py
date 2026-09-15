#!/usr/bin/env python3
"""Google Ads account review over normalized CSV exports (v2.0.0, 2026-09-15).

Six review areas from local CSV files. Writes a fresh output directory with findings.json (complete evidence),
negative_candidates.csv, change_list.md (review wording, nothing paste-ready) and manifest.json.
Reads local files only: no network, no credentials, no subprocesses, no Google Ads changes.

Input contract (documented in SKILL.md): UTF-8 CSV in English, one header row, no report preamble, no total
or subtotal rows, decimal point for numbers (comma thousands separators allowed), no currency symbols, no
blank required cells. A schema problem stops the run and names the file and row. Nothing is guessed to zero.
"""
import argparse, csv, json, math, re, sys
from pathlib import Path

VERSION = "2.0.0"
NUM = re.compile(r"[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")

# required and optional columns per file; aliases are explicit normalizations, never guesses
SCHEMA = {
    "conversions.csv": dict(required=["Conversion action", "Action optimization", "Conversions", "Conv. value"],
                            aliases={"Include in \"Conversions\"": "Action optimization", "Include in Conversions": "Action optimization",
                                     "Primary": "Action optimization", "Conversion value": "Conv. value"}),
    "search_terms.csv": dict(required=["Search term", "Campaign", "Cost", "Conversions", "Conv. value"],
                             aliases={"Conversion value": "Conv. value", "Search term match type": "Match type"}),
    "campaigns.csv": dict(required=["Campaign", "Campaign type", "Cost", "Conversions", "Conv. value"],
                          aliases={"Conversion value": "Conv. value"}),
    "products.csv": dict(required=["Item ID", "Title", "Cost", "Conversions", "Conv. value"],
                         aliases={"Conversion value": "Conv. value", "Item Id": "Item ID"}),
    "margins.csv": dict(required=["Item ID", "Margin"], aliases={"Item Id": "Item ID"}),
}
REQUIRED_FILES = ["conversions.csv", "search_terms.csv", "campaigns.csv"]
OPTIONAL_FILES = ["products.csv", "margins.csv"]
NUMERIC = {"Cost", "Conversions", "Conv. value", "Margin"}
MICRO = re.compile(r"page ?view|add.?to.?cart|view.?item|scroll|call|engag|session|lead form open", re.I)
PURCHASE = re.compile(r"purchase|\border\b|\bsale\b|\bsales\b|checkout complete|transaction", re.I)


class SchemaError(Exception):
    pass


def num(value, where):
    text = str(value).strip()
    if not NUM.fullmatch(text):
        raise SchemaError(f"{where}: invalid numeric value {value!r}. Use a decimal point, optional comma thousands "
                          "separators, no currency symbol; resolve blank or unavailable values before analysis.")
    result = float(text.replace(",", ""))
    if not math.isfinite(result):
        raise SchemaError(f"{where}: non-finite numeric value {value!r}")
    return result


def read(root, name, required):
    p = root / name
    if not p.is_file():
        if required:
            raise SchemaError(f"{name}: required file missing in {root}")
        return None
    spec = SCHEMA[name]
    with open(p, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise SchemaError(f"{name}: file is empty")
        norm = [spec["aliases"].get(h.strip(), h.strip()) for h in header]
        dupes = sorted({h for h in norm if norm.count(h) > 1})
        if dupes:
            raise SchemaError(f"{name}: duplicate header after normalization: {dupes}")
        missing = [c for c in spec["required"] if c not in norm]
        if missing:
            raise SchemaError(f"{name}: first row is not a usable header, missing column(s) {missing}. Remove any report "
                              "title or date preamble and normalize column names as documented in SKILL.md.")
        rows = []
        for i, raw in enumerate(reader, start=2):
            if not any(cell.strip() for cell in raw):
                continue
            if len(raw) > len(norm):
                raise SchemaError(f"{name} row {i}: {len(raw)} cells for {len(norm)} headers (overflow column)")
            if len(raw) < len(norm):
                raise SchemaError(f"{name} row {i}: {len(raw)} cells for {len(norm)} headers (short row)")
            row = dict(zip(norm, (c.strip() for c in raw)))
            first = raw[0].strip().casefold()
            if first.startswith("total") or first.startswith("subtotal"):
                raise SchemaError(f"{name} row {i}: total/subtotal row present; remove all total rows before the audit")
            for c in spec["required"]:
                if row[c] == "":
                    raise SchemaError(f"{name} row {i}: required column {c!r} is blank")
                if c in NUMERIC:
                    row["_" + c] = num(row[c], f"{name} row {i} column {c!r}")
            row["_row"] = i
            rows.append(row)
    if required and not rows:
        raise SchemaError(f"{name}: no data rows (header only); an empty required table cannot be audited")
    return rows


def brand_matcher(tokens):
    pats = [re.compile(r"(?<!\w)" + re.escape(t) + r"(?!\w)", re.I) for t in tokens]
    return lambda s: any(p.search(s or "") for p in pats)


def r2(x):
    return None if x is None else round(x, 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--input", type=Path, required=True, help="directory holding the normalized CSV exports")
    ap.add_argument("--out", type=Path, required=True, help="fresh output directory for this account and run (must not exist)")
    ap.add_argument("--brand", required=True, help="comma-separated brand phrases, matched as whole words")
    ap.add_argument("--currency", required=True, help="account currency code as exported, e.g. GBP")
    ap.add_argument("--account", required=True, help="account label from the intake record")
    ap.add_argument("--window-start", required=True, help="export start date YYYY-MM-DD from the intake record")
    ap.add_argument("--window-end", required=True, help="export end date YYYY-MM-DD from the intake record")
    a = ap.parse_args()
    for d in (a.window_start, a.window_end):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            ap.error(f"date {d!r} must be YYYY-MM-DD")
    root = a.input.expanduser().resolve()
    out = a.out.expanduser().resolve()
    if not root.is_dir():
        ap.error(f"--input {root} is not a directory")
    if out.exists():
        ap.error(f"--out {out} already exists; each run requires a new output directory")
    brand = [b.strip() for b in a.brand.split(",") if b.strip()]
    if not brand:
        ap.error("--brand needs at least one phrase")
    isb = brand_matcher(brand)

    # preflight: every file is validated before any output exists
    try:
        T = {name: read(root, name, required=True) for name in REQUIRED_FILES}
        T.update({name: read(root, name, required=False) for name in OPTIONAL_FILES})
        conv, st, camp, prod, marg = (T[n] for n in REQUIRED_FILES + OPTIONAL_FILES)

        campaign_types = {}
        for r in camp:
            key, value = r["Campaign"], r["Campaign type"].casefold()
            if key in campaign_types and campaign_types[key] != value:
                raise SchemaError(f"campaigns.csv: conflicting campaign types for {key!r}")
            campaign_types[key] = value
        missing_c = sorted({r["Campaign"] for r in st} - campaign_types.keys())
        if missing_c:
            raise SchemaError(f"search_terms.csv: campaigns missing from campaigns.csv: {missing_c}")

        for r in conv:
            opt = r["Action optimization"].strip().casefold()
            if opt in ("yes", "true"):
                opt = "primary"
            elif opt in ("no", "false"):
                opt = "secondary"
            if opt not in ("primary", "secondary"):
                raise SchemaError(f"conversions.csv row {r['_row']}: Action optimization must be Primary or Secondary, got {r['Action optimization']!r}")
            r["_opt"] = opt.capitalize()

        mmap = None
        if prod is not None:
            seen = set()
            for r in prod:
                if r["Item ID"] in seen:
                    raise SchemaError(f"products.csv: duplicate Item ID {r['Item ID']!r}; aggregate to one row per item before the audit")
                seen.add(r["Item ID"])
            if marg is not None:
                mmap = {}
                for r in marg:
                    if r["Item ID"] in mmap:
                        raise SchemaError(f"margins.csv: duplicate margin for item {r['Item ID']!r}")
                    if not 0 <= r["_Margin"] <= 1:
                        raise SchemaError(f"margins.csv row {r['_row']}: Margin for {r['Item ID']!r} must be a fraction from 0 to 1")
                    mmap[r["Item ID"]] = r["_Margin"]
                missing_m = sorted(seen - mmap.keys())
                if missing_m:
                    raise SchemaError(f"margins.csv: missing margins for items {missing_m}; supply them or rerun without margins.csv")
        elif marg is not None:
            raise SchemaError("margins.csv supplied without products.csv")
    except SchemaError as e:
        sys.exit(f"STOP: {e}")

    F = dict(version=VERSION, account=a.account, currency=a.currency,
             window=dict(start=a.window_start, end=a.window_end, source="intake record"),
             not_measured=[], notes=[
                 "Some queries are withheld for privacy, so visible search-term rows do not necessarily reconcile to campaign totals.",
                 "The review areas overlap: the same spend can appear in several lists. Do not sum them as independent waste."],
             review_actions=[])
    actions = []
    def action(fid, obj, evidence, proposed):
        actions.append(dict(finding_id=f"{fid}-{len(actions)+1:03d}", object=obj, evidence=evidence,
                            proposed_action=proposed, review_status="pending human review"))

    # 1 conversion configuration review
    prim = [r for r in conv if r["_opt"] == "Primary"]
    F["conversion_configuration"] = dict(
        actions=[dict(name=r["Conversion action"], optimization=r["_opt"], conversions=r["_Conversions"], value=r["_Conv. value"]) for r in conv],
        primary_count=len(prim), secondary_count=len(conv) - len(prim),
        micro_named_primary=[r["Conversion action"] for r in prim if MICRO.search(r["Conversion action"])],
        purchase_named_secondary=[r["Conversion action"] for r in conv if r["_opt"] == "Secondary" and PURCHASE.search(r["Conversion action"])],
        note="Names suggest an action's purpose; they do not verify its definition, duration or goal usage.",
        source_fields=["conversions.csv: Conversion action, Action optimization, Conversions, Conv. value"])
    F["not_measured"] += ["conversion configuration: campaign goal usage", "conversion configuration: custom-goal membership",
                          "conversion configuration: conversion definitions", "conversion configuration: configured call duration"]
    for n in F["conversion_configuration"]["micro_named_primary"]:
        action("CONV", n, "name suggests a micro-conversion and it is set to Primary", "review the action definition and goal usage before changing its optimization setting")
    for n in F["conversion_configuration"]["purchase_named_secondary"]:
        action("CONV", n, "name suggests a purchase and it is set to Secondary", "review whether a custom goal already uses it; do not change from the name alone")

    # 2 search terms
    for r in st:
        r["_brand"] = isb(r["Search term"])
    tot_cost = sum(r["_Cost"] for r in st); tot_conv = sum(r["_Conversions"] for r in st)
    agg_cpa = tot_cost / tot_conv if tot_conv else None
    def qrow(r, **extra):
        return dict(term=r["Search term"], campaign=r["Campaign"], match_type=r.get("Match type", ""), cost=r2(r["_Cost"]),
                    conversions=r["_Conversions"], value=r2(r["_Conv. value"]), brand_match=r["_brand"], **extra)
    zero = sorted([r for r in st if r["_Cost"] > 0 and r["_Conversions"] == 0], key=lambda r: -r["_Cost"])
    high = sorted([r for r in st if agg_cpa and r["_Conversions"] > 0 and r["_Cost"] / r["_Conversions"] > 3 * agg_cpa], key=lambda r: -r["_Cost"])
    def bucket(rows):
        c = sum(r["_Cost"] for r in rows); k = sum(r["_Conversions"] for r in rows)
        return dict(rows=len(rows), cost=r2(c), conversions=k, value=r2(sum(r["_Conv. value"] for r in rows)), cpa=r2(c / k) if k else None)
    F["search_terms"] = dict(
        returned_rows=len(st), returned_rows_cost=r2(tot_cost), returned_rows_conversions=tot_conv,
        returned_rows_cpa=r2(agg_cpa), cpa_note="aggregate CPA of the returned search-term rows, not account CPA",
        brand=bucket([r for r in st if r["_brand"]]), non_brand=bucket([r for r in st if not r["_brand"]]),
        split_note="brand/non-brand split of the returned query rows only; the broader account split is not measured",
        zero_conversion=[qrow(r) for r in zero], zero_conversion_cost=r2(sum(r["_Cost"] for r in zero)),
        high_cpa=[qrow(r, cpa=r2(r["_Cost"] / r["_Conversions"])) for r in high],
        high_cpa_rule="conversions > 0 and row CPA > 3 x returned-rows CPA; an Addition screening rule",
        source_fields=["search_terms.csv: Search term, Campaign, Match type, Cost, Conversions, Conv. value", "--brand phrases"])
    F["not_measured"].append("search terms: account-level brand/non-brand split (hidden terms, campaign types, goal differences)")
    for x in F["search_terms"]["zero_conversion"]:
        if not x["brand_match"]:
            action("QUERY", f"{x['term']} in {x['campaign']}", f"spent {x['cost']} {a.currency}, 0 recorded conversions in the window",
                   "check intent, measurement and conversion lag before approving an exact-match negative in this campaign")

    # 3 brand activity in Shopping and Performance Max
    leak = sorted([r for r in st if r["_brand"] and campaign_types[r["Campaign"]] in {"shopping", "performance max"}], key=lambda r: -r["_Cost"])
    F["brand_activity_shopping_pmax"] = dict(
        cost=r2(sum(r["_Cost"] for r in leak)), conversions=sum(r["_Conversions"] for r in leak), value=r2(sum(r["_Conv. value"] for r in leak)),
        rows=[qrow(r, campaign_type=campaign_types[r["Campaign"]]) for r in leak],
        note="attributed cost on reported queries matching the brand phrases in Shopping and Performance Max campaigns; not incremental sales, organic substitution or savings",
        source_fields=["search_terms.csv joined to campaigns.csv on Campaign; Campaign type in {shopping, performance max}", "--brand phrases"])
    F["not_measured"].append("brand activity: incrementality of brand coverage (requires a test)")
    if leak:
        action("BRAND", "brand queries in Shopping/PMax", f"{F['brand_activity_shopping_pmax']['cost']} {a.currency} attributed across {len(leak)} query rows",
               "review campaign roles and run an incrementality test before changing brand coverage")

    # 4 product contribution ranking
    prod_rows = []
    if prod is not None:
        for r in prod:
            c, v, k = r["_Cost"], r["_Conv. value"], r["_Conversions"]
            m = mmap[r["Item ID"]] if mmap is not None else None
            contrib = (v * m - c) if m is not None else (v - c)
            prod_rows.append(dict(item=r["Item ID"], title=r["Title"], cost=r2(c), conversions=k, value=r2(v), margin=m, contribution=r2(contrib)))
        prod_rows.sort(key=lambda x: x["contribution"])
        F["product_contribution"] = dict(
            basis="reported conversion value x supplied margin fraction - reported ad cost" if mmap is not None else "reported conversion value - reported ad cost (margins.csv not supplied)",
            basis_note="confirm the value is revenue on the same tax, refund and currency basis as the margin; this is not verified accounting profit",
            products=len(prod_rows), below_line=sum(1 for x in prod_rows if x["contribution"] < 0),
            ranking=prod_rows, source_fields=["products.csv: Item ID, Title, Cost, Conversions, Conv. value"] + (["margins.csv: Item ID, Margin"] if mmap is not None else []))
    else:
        F["product_contribution"] = None
        F["not_measured"].append("product contribution: export products.csv")

    # 5 repeat buyers: audience names alone cannot establish it
    F["repeat_buyers"] = None
    F["not_measured"].append("repeat buyers: audience names alone do not identify purchasers or prospecting spend; provide verified list "
                             "definitions, campaign purpose and non-overlapping reporting before calculating this check")

    # 6 silent killers: positive cost, zero recorded conversions, in the top floor(n/5) rows by cost or >= 5% of that report's cost
    def killers(rows, kind, name_key):
        rs = sorted(rows, key=lambda x: -x["cost"]); total = sum(x["cost"] for x in rs)
        top = {x[name_key] for x in rs[:max(1, len(rs) // 5)]}
        return [dict(kind=kind, name=x[name_key], cost=x["cost"], share=round(x["cost"] / total, 3) if total else None)
                for x in rs if x["conversions"] == 0 and x["cost"] > 0 and (x[name_key] in top or (total and x["cost"] / total >= 0.05))]
    camp_rows = [dict(name=r["Campaign"], cost=r2(r["_Cost"]), conversions=r["_Conversions"]) for r in camp]
    K = killers(camp_rows, "campaign", "name") + (killers(prod_rows, "product", "item") if prod_rows else [])
    F["silent_killers"] = dict(rows=sorted(K, key=lambda k: -k["cost"]),
                               rule="positive cost and zero recorded conversions, in the first max(1, floor(rows/5)) rows by descending cost or >= 5% of that report's cost; an Addition screening rule, not a statistical test; keywords are not checked",
                               source_fields=["campaigns.csv: Campaign, Cost, Conversions", "products.csv: Item ID, Cost, Conversions"])
    for k in F["silent_killers"]["rows"]:
        action("SILENT", f"{k['kind']} {k['name']}", f"{k['cost']} {a.currency} with 0 recorded conversions ({k['share']} of the report's cost)",
               "report the window and conversion lag, then review before proposing a pause")
    F["review_actions"] = actions

    # outputs, only after every check succeeded
    out.mkdir(parents=True, exist_ok=False)
    (out / "findings.json").write_text(json.dumps(F, indent=2, allow_nan=False))
    fields = ["campaign", "term", "match_type", "cost", "conversions", "status"]
    with (out / "negative_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); seen = set()
        for x in F["search_terms"]["zero_conversion"]:
            key = (x["campaign"], x["term"])
            if x["brand_match"] or key in seen:
                continue
            seen.add(key)
            w.writerow(dict(campaign=x["campaign"], term=x["term"], match_type="exact", cost=x["cost"], conversions=x["conversions"],
                            status="review intent, measurement and conversion lag"))
    lines = ["# Review list", "", f"Account {a.account} · window {a.window_start} to {a.window_end} · currency {a.currency}",
             "Nothing here is paste-ready. Every line is a review candidate with its evidence; approve before changing the account.", ""]
    for x in actions:
        lines.append(f"- {x['finding_id']} {x['object']}: {x['evidence']}. Proposed: {x['proposed_action']}.")
    lines += ["", "## Not measured"] + [f"- {n}" for n in F["not_measured"]]
    (out / "change_list.md").write_text("\n".join(lines) + "\n")
    manifest = dict(version=VERSION, account=a.account, currency=a.currency, window_start=a.window_start, window_end=a.window_end,
                    input=str(root), files={n: (len(T[n]) if T[n] is not None else None) for n in REQUIRED_FILES + OPTIONAL_FILES},
                    brand_phrases=brand, outputs=["findings.json", "negative_candidates.csv", "change_list.md", "manifest.json"])
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"conversion actions {len(prim)} primary / {len(conv) - len(prim)} secondary · zero-conversion query rows {len(zero)} "
          f"({F['search_terms']['zero_conversion_cost']} {a.currency}) · brand activity in Shopping/PMax {F['brand_activity_shopping_pmax']['cost']} "
          f"· silent killers {len(K)} · review actions {len(actions)} · not measured {len(F['not_measured'])} → {out}")


if __name__ == "__main__":
    main()
