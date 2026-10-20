# Farad Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from fractions import Fraction

C = "each capacitance must be from 0.01 to 100000 µF with at most two decimal places"
V = "the voltage must be from 0.01 to 1000 V with at most two decimal places"

def p(t, err, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v):
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def uf(c): return dec(c) + " µF"
def vv(x): return dec(x) + " V"
def uc(c100, v100): return dec(int(hu(Fraction(c100) * v100, 100))) + " µC"
def mj(c100, v100): return dec(int(hu(Fraction(c100) * v100 * v100, 20000000))) + " mJ"

def chargeTruth(volts, cap):
    v = p(volts, V, 1, 100000); a = p(cap, C, 1, 10000000)
    return "A " + uf(a) + " capacitor at " + vv(v) + " holds " + uc(a, v) + " of charge and " + mj(a, v) + " of energy."

def parallelTruth(volts, c1, c2):
    v = p(volts, V, 1, 100000); a = p(c1, C, 1, 10000000); b = p(c2, C, 1, 10000000)
    tot = a + b
    return uf(a) + " and " + uf(b) + " in parallel act like " + uf(tot) + ", holding " + uc(tot, v) + " at " + vv(v) + "."

def seriesTruth(volts, c1, c2):
    v = p(volts, V, 1, 100000); a = p(c1, C, 1, 10000000); b = p(c2, C, 1, 10000000)
    s = a + b
    eq = int(hu(Fraction(a) * b, s))
    q = int(hu(Fraction(a) * b * v, s * 100))
    v1 = int(hu(Fraction(v) * b, s)); v2 = int(hu(Fraction(v) * a, s))
    return uf(a) + " and " + uf(b) + " in series act like " + uf(eq) + ". At " + vv(v) + " the pair carries " + dec(q) + " µC, with " + vv(v1) + " on the " + uf(a) + " one and " + vv(v2) + " on the " + uf(b) + " one."

FNS = {"chargeTruth": chargeTruth, "parallelTruth": parallelTruth, "seriesTruth": seriesTruth}

cases = []
vs = ["0.01", "1.5", "5", "12", "400", "1000"]
cs = ["0.01", "0.1", "1", "47", "100", "1000", "99999.99", "100000"]
for v in vs:
    for c in cs:
        cases.append(("chargeTruth", [v, c]))
pairs = [("100", "47"), ("10", "10"), ("0.01", "100000"), ("220", "330"), ("1", "0.5")]
for v in vs:
    for a, b in pairs:
        cases.append(("parallelTruth", [v, a, b]))
        cases.append(("seriesTruth", [v, a, b]))
errs = [("0", "100"), ("1001", "100"), ("12", "0"), ("12", "100001"), ("1.234", "100"),
        ("12", "1.234"), ("x", "100"), ("12", ""), ("", "100")]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for v, c in errs:
    for name, args in [("chargeTruth", [v, c]), ("parallelTruth", [v, c, "47"]), ("seriesTruth", [v, "100", c])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
