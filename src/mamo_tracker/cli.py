"""CLI entrypoint."""

from __future__ import annotations

import argparse
import json
import sys

from .model import ModelParams, compute
from .report import format_dashboard
from .snapshot import load_snapshot


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mamo-tracker", description="MAMO Americas print model v2.1")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_comp = sub.add_parser("compute", help="Compute three-layer dashboard from a snapshot JSON")
    p_comp.add_argument("snapshot", help="Path to snapshot JSON")
    p_comp.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    p_comp.add_argument("--rho", type=float, default=None, help="Override reseller overlap ρ")
    p_comp.add_argument("--h", type=float, default=None, help="Override TCGP hobby share h")
    p_comp.add_argument("--C-M", dest="C_M", type=float, default=None, help="Override mass coverage C_M")
    p_comp.add_argument("--u", type=float, default=None, help="Override unsold factor u")

    p_sens = sub.add_parser("sensitivity", help="Print Target / h / C_M / ρ stress table")
    p_sens.add_argument("snapshot", help="Path to snapshot JSON")

    args = parser.parse_args(argv)
    inputs = load_snapshot(args.snapshot)

    if args.cmd == "compute":
        base = ModelParams()
        params = ModelParams(
            C_M=args.C_M if args.C_M is not None else base.C_M,
            h=args.h if args.h is not None else base.h,
            u=args.u if args.u is not None else base.u,
            rho=args.rho if args.rho is not None else base.rho,
        )
        result = compute(inputs, params)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, default=str))
        else:
            print(format_dashboard(result), end="")
        return 0

    if args.cmd == "sensitivity":
        print(_sensitivity_table(inputs))
        return 0

    return 1


def _sensitivity_table(inputs) -> str:
    from .model import SnapshotInputs

    rows = ["Target stress × knobs (S_est / P_est)", ""]
    targets = [40000, 62000, 80000, 100000]
    rows.append(f"{'Target':>8}  {'S_est':>10}  {'P_est':>10}")
    for t in targets:
        alt = SnapshotInputs(
            date=inputs.date,
            m_obs=float(t),
            tcg_boxes=inputs.tcg_boxes,
            tcg_displays=inputs.tcg_displays,
            a3p_box_bought=inputs.a3p_box_bought,
            a3p_display_bought=inputs.a3p_display_bought,
            notes=inputs.notes,
            confidence=inputs.confidence,
        )
        r = compute(alt)
        rows.append(f"{t:>8,}  {r.S_est:>10,.0f}  {r.P_est:>10,.0f}")

    rows += ["", "ρ band on A3P (base Target)", f"{'ρ':>6}  {'A3P_adj':>10}  {'S_est':>10}"]
    for rho in (0.03, 0.04, 0.05):
        r = compute(inputs, ModelParams(rho=rho))
        rows.append(f"{rho:>6.2f}  {r.A3P_adj:>10,.0f}  {r.S_est:>10,.0f}")
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
