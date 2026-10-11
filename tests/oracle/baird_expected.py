#!/usr/bin/env python3
"""Independent numpy check of the expected-update experiments on Baird's
counterexample (lib/algos/offpolicy-approx.aura): semi-gradient DP (Fig 11.2),
expected TDC (Fig 11.6) and expected emphatic TD (Fig 11.7), 1000 sweeps each.
Prints the values used in tests/test_ch11_baird.aura."""
import numpy as np

X = np.zeros((7, 8))
for i in range(6):
    X[i, i], X[i, 7] = 2, 1
X[6, 6], X[6, 7] = 1, 2
G, LOWER = 0.99, 6

def w0(): return np.array([1, 1, 1, 1, 1, 1, 10, 1.0])
def delta(w, s): return G * X[LOWER] @ w - X[s] @ w
def ve(w): return np.sqrt(np.mean((X @ w) ** 2))
def pbe(w): return np.sqrt(np.mean([delta(w, s) ** 2 for s in range(7)]))  # projection = I (rank 7)

w = w0()
for _ in range(1000):
    w = w + 0.01 * sum(delta(w, s) * X[s] for s in range(7)) / 7
print("DP     w =", w, "sqrt(VE) =", ve(w))

w, v = w0(), np.zeros(8)
for _ in range(1000):
    dw = sum(delta(w, s) * X[s] - G * X[LOWER] * (X[s] @ v) for s in range(7)) / 7
    dv = sum((delta(w, s) - v @ X[s]) * X[s] for s in range(7)) / 7
    w, v = w + 0.005 * dw, v + 0.05 * dv
print("TDC    w =", w, "sqrt(VE) =", ve(w), "sqrt(PBE) =", pbe(w))

w, M = w0(), 0.0
for _ in range(1000):
    up, Mn = np.zeros(8), 0.0
    for s in range(7):
        m = G * (7.0 if s == LOWER else 0.0) * M + 1.0   # rho of the step that entered s
        Mn += m / 7
        up += m * delta(w, s) * X[s] / 7
    w, M = w + 0.03 * up, Mn
print("ETD    w =", w, "sqrt(VE) =", ve(w), "M =", M)
