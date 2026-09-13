"""Format the three-layer dashboard."""

from __future__ import annotations

from .model import LayerResult


def _n(x: float) -> str:
    return f"{x:,.0f}"


def format_dashboard(r: LayerResult) -> str:
    p = r.params
    i = r.inputs
    lines = [
        "MAMO MODEL v2.1 — Americas sealed boxes",
        f"Snapshot date: {i.date}",
        f"Confidence:    {i.confidence}",
        "",
        "LAYER 1  Observed floor S_floor",
        f"  M_obs (1P mass):     {_n(i.m_obs)}",
        f"  H_tcgp:              {_n(r.H_tcgp)}",
        f"  A3P_raw:             {_n(r.A3P_raw)}",
        f"  S_floor:             {_n(r.S_floor)}+",
        "",
        "LAYER 2  Estimated sold S_est  ← dashboard primary",
        f"  A3P_adj (ρ={p.rho:.2f}): {_n(r.A3P_adj)}",
        f"  S_est:               {_n(r.S_est)}",
        f"  Sold band:           {_n(r.S_est_low)} – {_n(r.S_est_high)}",
        "",
        "LAYER 3  Estimated print P_est",
        f"  P_est (u={p.u:.2f}):     {_n(r.P_est)}",
        f"  Print band:          {_n(r.P_est_low)} – {_n(r.P_est_high)}",
        f"  US print (×{p.us_share}): {_n(r.P_US)}",
        "",
        "Knobs: "
        f"C_M={p.C_M}  h={p.h}  u={p.u}  ρ={p.rho}",
        "Note: A3P is NOT stretched by 1/h; only TCGP is.",
    ]
    if i.notes:
        lines.append("")
        lines.append("Notes:")
        for n in i.notes:
            lines.append(f"  - {n}")
    return "\n".join(lines) + "\n"
