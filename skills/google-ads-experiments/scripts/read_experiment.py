#!/usr/bin/env python3
"""Describe a completed Google Ads experiment from validated arm totals (v2.0.0, 2026-09-15).

Prints observed CPA or ROAS per arm and the relative difference. Descriptive comparison only: aggregate
totals do not provide a valid uncertainty estimate, and no apply decision is supported by this output alone.
Use the experiment's reported interval for the pre-registered metric together with the pre-registered
decision rule and a completed conversion-lag window.
Arm format: cost,conversions,value[,clicks]. Commas delimit fields, so thousands separators are not accepted.
"""
import argparse, math


def arm(text):
    parts = text.split(",")
    if len(parts) not in (3, 4):
        raise argparse.ArgumentTypeError("Use cost,conversions,value[,clicks]")
    try:
        values = [float(p.strip()) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use decimal-point numbers without currency symbols") from exc
    if any(not math.isfinite(v) or v < 0 for v in values):
        raise argparse.ArgumentTypeError("Values must be finite and non-negative")
    if values[0] <= 0:
        raise argparse.ArgumentTypeError("Cost must be greater than zero in both arms")
    return dict(cost=values[0], conv=values[1], value=values[2], clicks=values[3] if len(values) == 4 else None)


def main():
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--control", type=arm, required=True)
    a.add_argument("--trial", type=arm, required=True)
    a.add_argument("--metric", choices=["cpa", "roas"], required=True, help="the pre-registered decision metric")
    a.add_argument("--days", type=int, required=True, help="completed analysis duration in days (positive)")
    x = a.parse_args()
    C, T = x.control, x.trial
    if x.days <= 0:
        a.error("--days must be the positive completed analysis duration")
    if x.metric == "cpa":
        if C["conv"] == 0 or T["conv"] == 0:
            a.error("CPA is undefined for an arm with zero conversions")
        mc, mt, label = C["cost"] / C["conv"], T["cost"] / T["conv"], "CPA"
    else:
        mc, mt, label = C["value"] / C["cost"], T["value"] / T["cost"], "ROAS"
    line = (f"Trial {label} {mt:.2f} vs control {mc:.2f} over {x.days} days, "
            f"with {T['conv']:g} and {C['conv']:g} conversions")
    if mc == 0:
        line += " (relative difference is undefined because control is zero)."
    else:
        line += f" ({(mt - mc) / mc * 100:+.1f}%)."
    line += (" Descriptive comparison only. These aggregate totals do not provide a valid uncertainty estimate for "
             f"{label}. No apply decision is supported by this calculation alone.")
    print(line)


if __name__ == "__main__":
    main()
