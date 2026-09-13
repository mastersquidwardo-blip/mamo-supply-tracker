"""CLI entrypoint — plain English."""

from __future__ import annotations

import argparse
import json
import sys

from .holistic import compute_holistic
from .model import ModelParams, compute
from .report import format_dashboard
from .snapshot import load_snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mamo-tracker",
        description="MAMO Americas supply tracker (plain English)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_comp = sub.add_parser("compute", help="Core proven → estimated sold → print")
    p_comp.add_argument("snapshot", help="Path to snapshot JSON")
    p_comp.add_argument("--json", action="store_true")

    p_hol = sub.add_parser(
        "holistic",
        help="Core + hidden doors (Walmart/GameStop/Best Buy) + GMR serial bridge",
    )
    p_hol.add_argument("snapshot", help="Path to snapshot JSON")
    p_hol.add_argument(
        "--confirmed-americas",
        type=int,
        default=27,
        help="Confirmed Americas GMR serial identities from the serial tracker",
    )
    p_hol.add_argument("--json", action="store_true")

    p_sens = sub.add_parser("sensitivity", help="Target stress table")
    p_sens.add_argument("snapshot")

    args = parser.parse_args(argv)
    inputs = load_snapshot(args.snapshot)

    if args.cmd == "compute":
        result = compute(inputs)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, default=str))
        else:
            print(format_dashboard(result), end="")
        return 0

    if args.cmd == "holistic":
        h = compute_holistic(inputs, confirmed_americas_serials=args.confirmed_americas)
        if args.json:
            payload = {
                "proven_sold": h.core.S_floor,
                "estimated_sold_visible_only": h.core.S_est,
                "estimated_print_visible_only": h.core.P_est,
                "target_online": h.target_online,
                "target_total_with_instore": h.target_total_with_instore,
                "hidden_doors": list(h.hidden_doors),
                "other_mass": h.other_mass,
                "hidden_mass_total": h.hidden_mass_total,
                "estimated_sold_with_hidden": h.estimated_sold_with_hidden,
                "estimated_print_with_hidden": h.estimated_print_with_hidden,
                "gmr": h.gmr.__dict__,
            }
            print(json.dumps(payload, indent=2))
        else:
            print(_format_holistic(h), end="")
        return 0

    if args.cmd == "sensitivity":
        print(_sensitivity_table(inputs))
        return 0

    return 1


def _format_holistic(h) -> str:
    c = h.core
    lines = [
        "MAMO holistic view (labeled priors + GMR bridge)",
        "",
        "VISIBLE ONLY (no hidden-door guesses)",
        f"  Proven sold:              {c.S_floor:,.0f}+",
        f"  Estimated sold:           {c.S_est:,.0f}",
        f"  Estimated print:          {c.P_est:,.0f}",
        "",
        "HIDDEN MASS (guesses — not proven)",
        f"  Target online (badge):    {h.target_online:,.0f}",
        f"  Target with in-store:     {h.target_total_with_instore:,.0f}",
    ]
    for d in h.hidden_doors:
        lines.append(
            f"  {d['name']:<22} {d['total']:>8,.0f}  "
            f"(online {d['online']:,.0f} / in-store {d['in_store']:,.0f}; "
            f"{d['vs_target']:.0%} of Target total, {d['online_share']:.0%} online)"
        )
    lines += [
        f"  Other mass doors:         {h.other_mass:,.0f}",
        f"  Hidden mass add-on:       {h.hidden_mass_total:,.0f}",
        "",
        "WITH HIDDEN DOORS FOLDED IN",
        f"  Estimated sold:           {h.estimated_sold_with_hidden:,.0f}",
        f"  Estimated print:          {h.estimated_print_with_hidden:,.0f}",
        "",
        "GMR SERIAL BRIDGE (from confirmed Americas identities)",
        f"  Confirmed Americas:       {h.gmr.confirmed_americas_serials}",
        f"  Public report share mid:  {h.gmr.public_report_share:.0%}",
        f"  Implied pulled mid:       {h.gmr.implied_pulled:,.0f}",
        f"  Boxes per GMR @ print:    {h.gmr.boxes_per_gmr:,.1f}",
        f"  Implied boxes opened:     {h.gmr.implied_boxes_opened_mid:,.0f} "
        f"(band {h.gmr.implied_boxes_opened_low:,.0f} – {h.gmr.implied_boxes_opened_high:,.0f})",
        f"  Note: {h.gmr.note}",
        "",
    ]
    return "\n".join(lines)


def _sensitivity_table(inputs) -> str:
    from .model import SnapshotInputs

    rows = ["Target stress (visible-only S_est / P_est)", ""]
    rows.append(f"{'Target':>8}  {'Sold':>10}  {'Print':>10}")
    for t in (40000, 62000, 80000, 100000):
        alt = SnapshotInputs(
            date=inputs.date,
            m_obs=float(t),
            tcg_boxes=inputs.tcg_boxes,
            tcg_displays=inputs.tcg_displays,
            a3p_box_bought=inputs.a3p_box_bought,
            a3p_display_bought=inputs.a3p_display_bought,
        )
        r = compute(alt)
        rows.append(f"{t:>8,}  {r.S_est:>10,.0f}  {r.P_est:>10,.0f}")
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
