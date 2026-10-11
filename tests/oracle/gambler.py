#!/usr/bin/env python3
"""Gambler's problem (Example 4.3, p_h = 0.4) by in-place value iteration to
theta = 1e-9, for chapters/ch04_dp/gambler.aura. v(100) = 1, v(0) = 0. The printed
policy takes the smallest stake whose value is within 1e-6 of the best, as in
lib/envs/gambler.aura."""
import numpy as np

PH = 0.4
v = np.zeros(101); v[100] = 1.0
sweeps = 0; hist = {}
while True:
    sweeps += 1; d = 0.0
    for s in range(1, 100):
        best = max(PH * v[s + a] + (1 - PH) * v[s - a] for a in range(1, min(s, 100 - s) + 1))
        d = max(d, abs(best - v[s])); v[s] = best
    if sweeps <= 3:
        hist[sweeps] = v.copy()
    if d < 1e-9:
        break
print("sweeps", sweeps)
for k in (1, 2, 3):
    print("sweep", k, " ".join("%.6f" % hist[k][s] for s in (25, 50, 75, 99)))
print("final", " ".join("%.6f" % v[s] for s in (1, 10, 25, 50, 51, 75, 99)))
pol = []
for s in range(1, 100):
    qs = [PH * v[s + a] + (1 - PH) * v[s - a] for a in range(1, min(s, 100 - s) + 1)]
    m = max(qs)
    pol.append(next(a for a, x in zip(range(1, 101), qs) if x >= m - 1e-6))
print("policy", " ".join(map(str, pol)))
