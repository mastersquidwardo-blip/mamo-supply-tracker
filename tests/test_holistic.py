from mamo_tracker.gmr_bridge import bridge_from_confirmed
from mamo_tracker.holistic import compute_holistic
from mamo_tracker.model import SnapshotInputs
from mamo_tracker.snapshot import load_snapshot


SEED = SnapshotInputs(
    date="2026-09-11",
    m_obs=62000,
    tcg_boxes=2900,
    tcg_displays=2539,
    a3p_box_bought=2000,
    a3p_display_bought=200,
)


def test_gmr_bridge_bands():
    g = bridge_from_confirmed(27, 220110)
    assert g.boxes_per_gmr == 220110 / 1800
    assert g.implied_boxes_opened_low < g.implied_boxes_opened_mid < g.implied_boxes_opened_high


def test_holistic_hidden_positive():
    h = compute_holistic(SEED, confirmed_americas_serials=27)
    assert h.hidden_mass_total > 0
    assert h.estimated_sold_with_hidden > h.core.S_est
    assert h.gmr.confirmed_americas_serials == 27


def test_seed_file_loads():
    s = load_snapshot("data/snapshots/snapshot_2026-09-11.json")
    assert s.m_obs == 62000
