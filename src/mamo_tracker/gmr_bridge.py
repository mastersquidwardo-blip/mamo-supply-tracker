"""Bridge confirmed Grand Master Rare serials → box bands (plain English)."""

from __future__ import annotations

from dataclasses import dataclass


AMERICAS_GMR_LOCK = 1800


@dataclass(frozen=True)
class GmrBridgeParams:
    # Share of pulled Americas GMRs that become public confirmed identities
    public_report_share: float = 0.25  # mid; band 0.15–0.40
    public_report_share_low: float = 0.15  # fewer reported → more implied pulls
    public_report_share_high: float = 0.40
    # Boxes per GMR if print estimate is right (print / 1800)
    # Can also pass explicitly


@dataclass(frozen=True)
class GmrBridgeResult:
    confirmed_americas_serials: int
    americas_lock: int
    public_report_share: float
    implied_pulled: float
    boxes_per_gmr: float
    implied_boxes_opened_mid: float
    implied_boxes_opened_low: float
    implied_boxes_opened_high: float
    note: str


def bridge_from_confirmed(
    confirmed_americas_serials: int,
    estimated_print: float,
    params: GmrBridgeParams | None = None,
) -> GmrBridgeResult:
    """
    Confirmed public Americas serials → implied boxes opened band.

    This is NOT boxes sold (many boxes stay sealed). It bounds how many boxes
    were likely *opened* to produce the public serial sample, given a report share.
    """
    p = params or GmrBridgeParams()
    boxes_per = estimated_print / AMERICAS_GMR_LOCK if estimated_print > 0 else float("nan")

    def opened(share: float) -> float:
        share = min(max(share, 0.01), 0.95)
        pulled = confirmed_americas_serials / share
        return pulled * boxes_per

    mid = opened(p.public_report_share)
    # Low public share → more pulled → more boxes; high share → fewer boxes
    low = opened(p.public_report_share_high)
    high = opened(p.public_report_share_low)

    return GmrBridgeResult(
        confirmed_americas_serials=confirmed_americas_serials,
        americas_lock=AMERICAS_GMR_LOCK,
        public_report_share=p.public_report_share,
        implied_pulled=confirmed_americas_serials / p.public_report_share,
        boxes_per_gmr=boxes_per,
        implied_boxes_opened_mid=mid,
        implied_boxes_opened_low=min(low, high),
        implied_boxes_opened_high=max(low, high),
        note=(
            "Uses confirmed Americas serial identities from the serial tracker. "
            "Bands boxes opened, not boxes sold. Europe E-serials excluded."
        ),
    )
