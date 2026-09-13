from mamo_tracker.model import ModelParams, SnapshotInputs, compute
from mamo_tracker.snapshot import parse_snapshot


SEED = SnapshotInputs(
    date="2026-09-11",
    m_obs=62000,
    tcg_boxes=2900,
    tcg_displays=2539,
    a3p_box_bought=2000,
    a3p_display_bought=200,
)


def test_seed_ballpark():
    r = compute(SEED)
    assert r.H_tcgp == 28290
    assert r.A3P_raw == 4000
    assert abs(r.A3P_adj - 3840) < 1e-6
    assert r.S_floor == 94290
    assert abs(r.S_est - 191400) < 1e-6
    assert abs(r.P_est - 220110) < 1e-6
    assert abs(r.P_US - 220110 * 0.88) < 1e-6


def test_a3p_not_stretched_by_h():
    """Changing h must not scale A3P the way it scales TCGP."""
    base = compute(SEED, ModelParams(h=0.25))
    low_h = compute(SEED, ModelParams(h=0.20))
    # TCGP contribution rises when h falls
    assert low_h.S_est > base.S_est
    # A3P_adj unchanged when only h changes
    assert abs(low_h.A3P_adj - base.A3P_adj) < 1e-9
    delta = low_h.S_est - base.S_est
    expected_tcgp_delta = 28290 / 0.20 - 28290 / 0.25
    assert abs(delta - expected_tcgp_delta) < 1e-6


def test_rho_band():
    r03 = compute(SEED, ModelParams(rho=0.03))
    r05 = compute(SEED, ModelParams(rho=0.05))
    assert r03.A3P_adj > r05.A3P_adj
    assert r03.S_est > r05.S_est


def test_parse_snapshot_roundtrip():
    data = {
        "date": "2026-09-11",
        "m_obs": 62000,
        "tcg_boxes": 2900,
        "tcg_displays": 2539,
        "a3p_box_bought": 2000,
        "a3p_display_bought": 200,
        "notes": ["x"],
    }
    s = parse_snapshot(data)
    assert s.a3p_box_bought == 2000
