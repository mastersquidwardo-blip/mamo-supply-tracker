# Hidden channels (Walmart, GameStop, Best Buy, in-store)

We do **not** pretend these are proven sold. They are **labeled guesses** so the model can talk about boxes we cannot see online.

## Why this exists

- Walmart and GameStop often show **no sold count**.
- Best Buy sells MAMO **in store** even when online is thin or not clearly first-party.
- Target’s “62k+ bought” is mostly an **online** signal; stores can add more.

## Default guesses (editable)

Start from **Target total** after lifting the online badge for in-store Target:

| Door | vs Target total | Online share | Rest |
|---|---|---|---|
| Target | 1.00 (anchor) | 55% online | 45% in-store |
| Walmart | 75% | 45% online | 55% in-store |
| GameStop | 15% | 35% online | 65% in-store |
| Best Buy | 25% | 30% online | 70% in-store |
| Other mass | 10% | — | regional / missed |

These are **knobs**, not facts. Change them when you get cart-caps, store checks, or better badges.

## How they enter the math

1. Proven sold stays evidence-only (Target badge + TCGPlayer + Amazon marketplace).
2. Holistic estimated sold rebuilds mass using Target-with-in-store + Walmart + GameStop + Best Buy + other.
3. Print = that sold estimate × unsold-in-channel factor.

## Online vs in-store

For each door:

```
door total = online boxes ÷ online share
in-store boxes = door total − online boxes
```

If we only ever see online, a 30% online share means in-store is more than double the online piece.
