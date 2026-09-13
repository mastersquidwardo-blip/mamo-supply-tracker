# MAMO model v2.1

Three layers. Do not mash sold, unobserved sold, and in-channel inventory into one multiplier.

## Layer 1 — Observed floor

```
H_tcgp = TCGP_boxes + TCGP_displays × 10
A3P_raw = A3P_box_bought + A3P_display_bought × 10
H_vis = H_tcgp + A3P_raw
S_floor = M_obs + H_vis
```

Unknown doors stay unknown (omit), not zero-filled.

## Layer 2 — Estimated sold (dashboard primary)

```
A3P_adj = A3P_raw × (1 − ρ)
S_est = (M_obs × C_M) + (H_tcgp / h) + A3P_adj
```

**Stretch only TCGP by `1/h`.** Amazon 3P is already an observed channel, so it is not expanded again.

### Why A3P counts
Distinct completed checkouts on Amazon 3P vs TCGPlayer are distinct transactions. At ~$35 MSRP / ~$42 market, flipping TCGP→Amazon after fees/tax/shipping is generally not viable. Reseller overlap is treated as a **3–5% anomaly** (`ρ`), not a rule that “3P = double count.”

## Layer 3 — Estimated print

```
P_est = S_est × (1 + u)
P_US = P_est × 0.88
```

`u` is estimated unsold / in-channel relative to cumulative sold (weakest knob).

## Defaults

| Knob | Default | Band |
|------|---------|------|
| C_M | 1.20 | 1.15–1.25 |
| h | 0.25 | 0.20–0.30 |
| u | 0.15 | — |
| ρ | 0.04 | 0.03–0.05 |
