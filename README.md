# mamo-supply-tracker

Americas **Magnificent Monsters (MAMO)** sealed-box sell-through → print tracker.

Implements **model v2.1**:

1. **Observed floor** `S_floor` — evidence only (Target 1P + TCGPlayer + Amazon 3P bought)
2. **Estimated sold** `S_est` — dashboard primary
3. **Estimated print** `P_est` — sold × in-channel unsold factor

Amazon 3P **counts**, with a small reseller-overlap haircut `ρ` (3–5%). TCGPlayer is still stretched by `1/h`; A3P is **not**.

## Quick start

```bash
python -m pip install -e ".[dev]"
mamo-tracker compute data/snapshots/snapshot_2026-09-11.json
mamo-tracker sensitivity data/snapshots/snapshot_2026-09-11.json
pytest
```

## Seed snapshot (2026-09-11)

| Input | Value |
|-------|-------|
| Target 1P | 62,000+ |
| TCGP boxes | 2,900 |
| TCGP displays | 2,539 (= 25,390 boxes) |
| Amazon 3P | 2,000 + 200×10 = 4,000 (badge floors) |
| Amazon 1P / WMT / GS | 0 / unknown / unknown |

See [docs/FORMULA.md](docs/FORMULA.md) and [docs/GUARDRAILS.md](docs/GUARDRAILS.md).
