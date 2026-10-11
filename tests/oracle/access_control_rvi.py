#!/usr/bin/env python3
"""Optimal average reward and policy of the access-control queuing task
(Example 10.2) by relative value iteration, for chapters/ch10_onpolicy_control/
access_control.aura. Dynamics as in lib/algos/diff-sarsa.aura: accepting takes a
free server and pays the priority; then each busy server frees with p = 0.06; the
next priority is uniform over 1, 2, 4, 8."""
from math import comb
import numpy as np

N, P_FREE, PRI = 10, 0.06, [1, 2, 4, 8]

def backup(h):
    nh, pol = np.zeros_like(h), np.zeros(h.shape, dtype=int)
    for k in range(N + 1):
        for i, pr in enumerate(PRI):
            best, ba = None, 0
            for a in ([0, 1] if k > 0 else [0]):
                k1, busy = k - a, N - (k - a)
                ev = sum(comb(busy, j) * P_FREE ** j * (1 - P_FREE) ** (busy - j) * h[k1 + j].mean()
                         for j in range(busy + 1))
                q = pr * a + ev
                if best is None or q > best:
                    best, ba = q, a
            nh[k, i], pol[k, i] = best, ba
    return nh, pol

h = np.zeros((N + 1, 4))
for _ in range(100000):
    nh, pol = backup(h)
    gain = nh[0, 0] - h[0, 0]
    nh -= nh[0, 0]
    if np.abs(nh - h).max() < 1e-12:
        break
    h = nh
print("optimal average reward", gain)
print("policy (rows priority 8, 4, 2, 1; columns free servers 0..10; 1 = accept)")
for i in (3, 2, 1, 0):
    print(PRI[i], pol[:, i])
