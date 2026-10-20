# Farad Math

Capacitor arithmetic. A 100 µF capacitor at 12 V holds 1200 µC and 7.2 mJ. In series with a 47 µF one, the pair acts like 31.97 µF and the smaller one takes 8.16 V.

## What it computes

- **The charge truth** - charge (µC) and energy (mJ) on one capacitor (0.01 to 100000 µF) at a voltage (0.01 to 1000 V).
- **The parallel truth** - two capacitors in parallel: their combined capacitance and the charge they hold.
- **The series truth** - two capacitors in series: their combined capacitance, the charge the pair carries, and how the voltage splits across them.

## Boundary

Arithmetic only. The capacitances and the voltage are the owner's own entries, every capacitor treated as exact, full and ideal. It has not seen any circuit and does not know parts' tolerance, leakage or age, prior charge, the source's behavior or what anything is rated for, and it gives no verdict that a circuit is adequate or safe. A charged capacitor can hold energy after power is off. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a µF and of a V, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/faradmath/
Repo: https://github.com/iLanis-agent/faradmath
