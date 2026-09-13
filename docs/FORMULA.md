# Formula (plain English)

## Proven sold (floor)

```
TCGPlayer boxes = TCGPlayer box solds + (TCGPlayer display solds × 10)
Amazon marketplace boxes = marketplace box “bought” + (marketplace display “bought” × 10)
Proven sold = mass first-party + TCGPlayer boxes + Amazon marketplace boxes
```

Unknown doors (Walmart, GameStop with no numbers) stay **blank**, not zero.

## Estimated sold (main number)

```
Marketplace after overlap cushion = Amazon marketplace boxes × (1 − 0.04)
Estimated sold =
    (mass first-party × 1.20)
  + (TCGPlayer boxes ÷ 0.25)
  + Marketplace after overlap cushion
```

| Plain knob | Default | Band | Meaning |
|---|---|---|---|
| Mass coverage | 1.20 | 1.15–1.25 | Missed first-party doors |
| TCGPlayer share of remaining hobby | 25% | 20–30% | Only stretches TCGPlayer |
| Marketplace overlap cushion | 4% | 3–5% | Rare flipper double-ticks |
| Unsold still in channel | 15% | — | Used for print, not for “sold” |

## Estimated print

```
Estimated print = Estimated sold × 1.15
US print ≈ Estimated print × 0.88
```

## Why marketplace sales count

A finished Amazon marketplace checkout is a different sale from a TCGPlayer checkout. At ~$35 retail and ~$42 market, flipping between them after fees usually loses money. We still leave a **3–5% cushion** for weird flipper cases — not a rule that marketplace never counts.
