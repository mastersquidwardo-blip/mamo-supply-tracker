"""Hidden mass doors and online-vs-store ratios (labeled priors)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HiddenDoorPrior:
    """A retailer we do not have a sold badge for yet."""

    name: str
    # Share of Target first-party as a starting guess (1.0 = same as Target)
    vs_target: float
    # Fraction of that door's sales that happen online (rest = in-store / invisible)
    online_share: float
    note: str = ""


@dataclass(frozen=True)
class HiddenMassParams:
    """Priors for channels we cannot fully see online."""

    # If Target's badge is mostly online, scale up for in-store Target too
    target_online_share: float = 0.55  # online half-ish; rest in-store
    walmart: HiddenDoorPrior = HiddenDoorPrior(
        "Walmart",
        vs_target=0.75,
        online_share=0.45,
        note="No sold badge; mid prior vs Target",
    )
    gamestop: HiddenDoorPrior = HiddenDoorPrior(
        "GameStop",
        vs_target=0.15,
        online_share=0.35,
        note="Smaller door count; no usable sold count",
    )
    best_buy: HiddenDoorPrior = HiddenDoorPrior(
        "Best Buy",
        vs_target=0.25,
        online_share=0.30,
        note="In-store heavy; online often thin / not first-party verified",
    )
    other_mass_vs_target: float = 0.10  # Meijer / regional / etc.


def expand_target_for_instore(target_observed: float, online_share: float) -> tuple[float, float]:
    """Return (online_part, total_including_instore)."""
    share = min(max(online_share, 0.05), 0.95)
    total = target_observed / share
    return target_observed, total


def hidden_door_total(target_total: float, door: HiddenDoorPrior) -> dict:
    total = target_total * door.vs_target
    online = total * door.online_share
    instore = total - online
    return {
        "name": door.name,
        "total": total,
        "online": online,
        "in_store": instore,
        "vs_target": door.vs_target,
        "online_share": door.online_share,
        "note": door.note,
    }
