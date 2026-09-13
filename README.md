# MAMO Americas supply tracker

Public living tracker for **Yu-Gi-Oh! Magnificent Monsters** Americas tuck boxes.

**Dashboard:** https://mastersquidwardo-blip.github.io/mamo-supply-tracker/  
**Sister serial tracker:** https://mastersquidwardo-blip.github.io/mamo/

## Layers (plain English)

1. **Proven sold** — Target badge + TCGPlayer + Amazon marketplace  
2. **Estimated sold (visible)** — main online-evidence number  
3. **Hidden doors** — Walmart / GameStop / Best Buy / in-store ratios as **labeled guesses**  
4. **Estimated print** — sold + still in channel  
5. **GMR bridge** — confirmed Americas serials → implied boxes opened (± tolerance)

## CLI

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
mamo-tracker compute data/snapshots/snapshot_2026-09-11.json
mamo-tracker holistic data/snapshots/snapshot_2026-09-11.json --confirmed-americas 27
pytest
```

## Docs

- [Scope](docs/SCOPE.md)
- [Formula](docs/FORMULA.md)
- [Hidden channels](docs/HIDDEN-CHANNELS.md)
- [GMR bridge](docs/GMR-BRIDGE.md)
- [GMR check](docs/GMR-CHECK.md)

Not affiliated with Konami.
