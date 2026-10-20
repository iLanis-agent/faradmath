// Farad Math engine: charge and energy on one capacitor, two in parallel, two in series with the voltage split. Exact integers (hundredths of a uF, hundredths of a V), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _C = "each capacitance must be from 0.01 to 100000 µF with at most two decimal places";
var _V = "the voltage must be from 0.01 to 1000 V with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _uf(c) { return _dec(c, 2) + " µF"; }
function _v(v) { return _dec(v, 2) + " V"; }
function _uc(c100, v100) { return _dec(_hu(c100 * v100, 100), 2) + " µC"; } // hundredths of a µC
function _mj(c100, v100) { return _dec(_hu(c100 * v100 * v100, 20000000), 2) + " mJ"; } // hundredths of a mJ
function _in(v, c1, c2) {
  var out = { v: _p(v, _V, 4, 2, 1, 100000), a: _p(c1, _C, 6, 2, 1, 10000000) };
  if (c2 !== undefined) out.b = _p(c2, _C, 6, 2, 1, 10000000);
  return out;
}

function chargeTruth(volts, cap) {
  var p = _in(volts, cap);
  return "A " + _uf(p.a) + " capacitor at " + _v(p.v) + " holds " + _uc(p.a, p.v) + " of charge and " + _mj(p.a, p.v) + " of energy.";
}
function parallelTruth(volts, c1, c2) {
  var p = _in(volts, c1, c2), tot = p.a + p.b;
  return _uf(p.a) + " and " + _uf(p.b) + " in parallel act like " + _uf(tot) + ", holding " + _uc(tot, p.v) + " at " + _v(p.v) + ".";
}
function seriesTruth(volts, c1, c2) {
  var p = _in(volts, c1, c2), s = p.a + p.b;
  var eq = _hu(p.a * p.b, s); // display only
  var q = _hu(p.a * p.b * p.v, s * 100); // hundredths of a µC, exact ratio
  var v1 = _hu(p.v * p.b, s), v2 = _hu(p.v * p.a, s);
  return _uf(p.a) + " and " + _uf(p.b) + " in series act like " + _uf(eq) + ". At " + _v(p.v) + " the pair carries " + _dec(q, 2) + " µC, with " + _v(v1) + " on the " + _uf(p.a) + " one and " + _v(v2) + " on the " + _uf(p.b) + " one.";
}
