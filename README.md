# MAMO Americas supply tracker

Public living tracker for **Yu-Gi-Oh! Magnificent Monsters** Americas tuck-box print, from observable sell-through.

**Dashboard (GitHub Pages):** https://mastersquidwardo-blip.github.io/mamo-supply-tracker/

## Plain-English layers

| Name | Meaning |
|---|---|
| **Proven sold** | Evidence only (Target + TCGPlayer + Amazon marketplace) |
| **Estimated sold** | Main number — fills gaps we can’t see |
| **Estimated print** | Sold + stock still in the channel |

Amazon marketplace sales **count**, with a **3–5% overlap cushion** for rare flippers — not a rule that marketplace = double count.

## Quick start (CLI)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
mamo-tracker compute data/snapshots/snapshot_2026-09-11.json
pytest
```

## Grand Master Rare

Americas lock = **1,800** serials. At ~220k print that is ~**1 per 122 boxes**, not 1-in-881. See [GMR check](docs/GMR-CHECK.md).

## Docs

- [Scope](docs/SCOPE.md)
- [Formula](docs/FORMULA.md)
- [Guardrails](docs/GUARDRAILS.md)

Not affiliated with Konami.
