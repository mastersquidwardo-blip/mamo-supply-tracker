"""MAMO model v2.1 — three layers: floor → sold → print."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class ModelParams:
    """Defaults and sensitivity knobs."""

    C_M: float = 1.20
    h: float = 0.25
    u: float = 0.15
    rho: float = 0.04  # A3P reseller-overlap haircut (3–5% band)
    us_share: float = 0.88
    C_M_low: float = 1.15
    C_M_high: float = 1.25
    h_low: float = 0.20  # aggressive sold (smaller h → larger H_est)
    h_high: float = 0.30  # conservative sold
    rho_low: float = 0.03
    rho_high: float = 0.05


@dataclass(frozen=True)
class SnapshotInputs:
    """Observed inputs for one dated pull. Unknown doors omitted (not zero-filled)."""

    date: str
    m_obs: float  # observed 1P mass (Target, Amazon 1P, etc.)
    tcg_boxes: float
    tcg_displays: float
    a3p_box_bought: float = 0.0
    a3p_display_bought: float = 0.0
    notes: tuple[str, ...] = ()
    confidence: str = "medium"


@dataclass(frozen=True)
class LayerResult:
    H_tcgp: float
    A3P_raw: float
    A3P_adj: float
    H_vis: float
    S_floor: float
    S_est: float
    S_est_low: float
    S_est_high: float
    P_est: float
    P_est_low: float
    P_est_high: float
    P_US: float
    params: ModelParams
    inputs: SnapshotInputs

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


def _sold(m_obs: float, H_tcgp: float, A3P_raw: float, C_M: float, h: float, rho: float) -> float:
    """S_est: stretch ONLY TCGP by 1/h; A3P gets rho haircut only."""
    if h <= 0:
        raise ValueError("h must be > 0")
    A3P_adj = A3P_raw * (1.0 - rho)
    return (m_obs * C_M) + (H_tcgp / h) + A3P_adj


def compute(inputs: SnapshotInputs, params: ModelParams | None = None) -> LayerResult:
    """Compute three-layer Americas print model v2.1."""
    p = params or ModelParams()
    H_tcgp = inputs.tcg_boxes + inputs.tcg_displays * 10.0
    A3P_raw = inputs.a3p_box_bought + inputs.a3p_display_bought * 10.0
    A3P_adj = A3P_raw * (1.0 - p.rho)
    H_vis = H_tcgp + A3P_raw
    S_floor = inputs.m_obs + H_vis

    S_est = _sold(inputs.m_obs, H_tcgp, A3P_raw, p.C_M, p.h, p.rho)
    # Low sold: high h, low C_M, high rho (more haircut)
    S_est_low = _sold(inputs.m_obs, H_tcgp, A3P_raw, p.C_M_low, p.h_high, p.rho_high)
    # High sold: low h, high C_M, low rho
    S_est_high = _sold(inputs.m_obs, H_tcgp, A3P_raw, p.C_M_high, p.h_low, p.rho_low)

    P_est = S_est * (1.0 + p.u)
    P_est_low = S_est_low * (1.0 + p.u)
    P_est_high = S_est_high * (1.0 + p.u)
    P_US = P_est * p.us_share

    return LayerResult(
        H_tcgp=H_tcgp,
        A3P_raw=A3P_raw,
        A3P_adj=A3P_adj,
        H_vis=H_vis,
        S_floor=S_floor,
        S_est=S_est,
        S_est_low=S_est_low,
        S_est_high=S_est_high,
        P_est=P_est,
        P_est_low=P_est_low,
        P_est_high=P_est_high,
        P_US=P_US,
        params=p,
        inputs=inputs,
    )
