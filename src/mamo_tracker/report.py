"""Format the three-layer dashboard in plain English."""

from __future__ import annotations

from .model import LayerResult


def _n(x: float) -> str:
    return f"{x:,.0f}"


def format_dashboard(r: LayerResult) -> str:
    p = r.params
    i = r.inputs
    lines = [
        "MAMO Americas supply tracker",
        f"Snapshot date: {i.date}",
        f"Confidence:    {i.confidence}",
        "",
        "PROVEN SOLD (floor — not a guess)",
        f"  Mass first-party:           {_n(i.m_obs)}",
        f"  TCGPlayer boxes seen:       {_n(r.H_tcgp)}",
        f"  Amazon marketplace seen:    {_n(r.A3P_raw)}",
        f"  Proven sold:                {_n(r.S_floor)}+",
        "",
        "ESTIMATED SOLD  ← main dashboard number",
        f"  Marketplace after {p.rho*100:.0f}% cushion: {_n(r.A3P_adj)}",
        f"  Estimated sold:             {_n(r.S_est)}",
        f"  Sold band:                  {_n(r.S_est_low)} – {_n(r.S_est_high)}",
        "",
        "ESTIMATED PRINT",
        f"  Unsold still in channel:    {p.u*100:.0f}%",
        f"  Estimated print:            {_n(r.P_est)}",
        f"  Print band:                 {_n(r.P_est_low)} – {_n(r.P_est_high)}",
        f"  US print:                   {_n(r.P_US)}",
        "",
        "Knobs (plain): "
        f"mass coverage={p.C_M}, "
        f"TCGPlayer hobby share={p.h}, "
        f"unsold in channel={p.u}, "
        f"marketplace overlap cushion={p.rho}",
        "Note: marketplace is NOT stretched like TCGPlayer; only TCGPlayer uses ÷ hobby share.",
    ]
    if i.notes:
        lines.append("")
        lines.append("Notes:")
        for n in i.notes:
            lines.append(f"  - {n}")
    return "\n".join(lines) + "\n"
