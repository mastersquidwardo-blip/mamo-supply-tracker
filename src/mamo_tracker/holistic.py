"""Holistic week-1 view: proven + hidden mass + GMR opened-box bridge."""

from __future__ import annotations

from dataclasses import dataclass

from .channels import HiddenMassParams, expand_target_for_instore, hidden_door_total
from .gmr_bridge import GmrBridgeParams, GmrBridgeResult, bridge_from_confirmed
from .model import ModelParams, SnapshotInputs, LayerResult, compute


@dataclass(frozen=True)
class HolisticResult:
    core: LayerResult
    target_online: float
    target_total_with_instore: float
    hidden_doors: tuple[dict, ...]
    other_mass: float
    hidden_mass_total: float
    estimated_sold_with_hidden: float
    estimated_print_with_hidden: float
    gmr: GmrBridgeResult


def compute_holistic(
    inputs: SnapshotInputs,
    confirmed_americas_serials: int = 27,
    model_params: ModelParams | None = None,
    hidden_params: HiddenMassParams | None = None,
    gmr_params: GmrBridgeParams | None = None,
) -> HolisticResult:
    mp = model_params or ModelParams()
    hp = hidden_params or HiddenMassParams()
    core = compute(inputs, mp)

    # Target badge → online observed; expand for in-store Target
    target_online, target_total = expand_target_for_instore(
        inputs.m_obs, hp.target_online_share
    )
    target_instore = target_total - target_online

    doors = (
        hidden_door_total(target_total, hp.walmart),
        hidden_door_total(target_total, hp.gamestop),
        hidden_door_total(target_total, hp.best_buy),
    )
    other = target_total * hp.other_mass_vs_target
    # Hidden = Target in-store add-on + other doors + other mass
    # (Target online already in proven m_obs)
    hidden = target_instore + sum(d["total"] for d in doors) + other

    # Rebuild estimated sold with expanded mass first-party
    m_obs_expanded = target_total + sum(d["total"] for d in doors) + other
    expanded_inputs = SnapshotInputs(
        date=inputs.date,
        m_obs=m_obs_expanded,
        tcg_boxes=inputs.tcg_boxes,
        tcg_displays=inputs.tcg_displays,
        a3p_box_bought=inputs.a3p_box_bought,
        a3p_display_bought=inputs.a3p_display_bought,
        notes=inputs.notes + ("Includes labeled hidden-mass priors",),
        confidence=inputs.confidence,
    )
    expanded = compute(expanded_inputs, mp)
    gmr = bridge_from_confirmed(confirmed_americas_serials, expanded.P_est, gmr_params)

    return HolisticResult(
        core=core,
        target_online=target_online,
        target_total_with_instore=target_total,
        hidden_doors=doors,
        other_mass=other,
        hidden_mass_total=hidden,
        estimated_sold_with_hidden=expanded.S_est,
        estimated_print_with_hidden=expanded.P_est,
        gmr=gmr,
    )
