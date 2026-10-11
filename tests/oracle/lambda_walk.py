#!/usr/bin/env python3
"""Independent Python check of lib/algos/traces.aura (Chapter 12, 19-state walk).

Replays the same Park-Miller PRNG as lib/rl/rng.aura so that a given seed gives the
same episodes; prints the mean RMS error over runs x episodes for a few
(method, lambda, alpha) configurations. Used to set the expected values in
tests/test_ch12_traces.aura.
"""
import math

M = 2147483647
class Rng:
    def __init__(self, s): self.s = 1 + s % (M - 1)
    def next(self): self.s = (16807 * self.s) % M; return self.s
    def int(self, n): return self.next() % n

TRUTH = [0.0] + [-1 + 2 * s / 20 for s in range(1, 20)] + [0.0]

def gen(rng, n):
    eps = []
    for _ in range(n):
        s, traj = 10, []
        while True:
            traj.append(s)
            s2 = s - 1 if rng.int(2) == 0 else s + 1
            if s2 == 0: eps.append((traj, -1.0)); break
            if s2 == 20: eps.append((traj, 1.0)); break
            s = s2
    return eps

def rms(v): return math.sqrt(sum((v[s] - TRUTH[s]) * (v[s] - TRUTH[s]) for s in range(1, 20)) / 19)

def offline(v, traj, R, lam, a):
    snap, T = v[:], len(traj)
    g = [0.0] * T; g[T - 1] = R
    for t in range(T - 2, -1, -1): g[t] = (1 - lam) * snap[traj[t + 1]] + lam * g[t + 1]
    for t in range(T): s = traj[t]; v[s] += a * (g[t] - v[s])

def tdl(v, traj, R, lam, a):
    z, T = [0.0] * 21, len(traj)
    for t in range(T):
        s = traj[t]; last = t == T - 1
        d = (R if last else 0.0) + (0.0 if last else v[traj[t + 1]]) - v[s]
        z = [lam * x for x in z]; z[s] += 1
        for i in range(1, 20): v[i] += a * d * z[i]

def tol(v, traj, R, lam, a):
    z, T, vold = [0.0] * 21, len(traj), 0.0
    for t in range(T):
        s = traj[t]; last = t == T - 1
        V = v[s]; Vn = 0.0 if last else v[traj[t + 1]]
        d = (R if last else 0.0) + Vn - V
        zs = z[s]; z = [lam * x for x in z]; z[s] += 1 - a * lam * zs
        for i in range(1, 20): v[i] += a * (d + V - vold) * z[i]
        v[s] -= a * (V - vold); vold = Vn

def run(seed, runs, n, configs):
    rng = Rng(seed); tot = [0.0] * len(configs)
    for _ in range(runs):
        eps = gen(rng, n)
        for j, (m, lam, a) in enumerate(configs):
            v = [0.0] * 21
            for traj, R in eps:
                [offline, tdl, tol][m](v, traj, R, lam, a)
                e = rms(v); tot[j] += e if e < 1.0 else 1.0  # NaN compares false -> 1.0
    return [x / (runs * n) for x in tot]

if __name__ == "__main__":
    cfg = [(0, 0.8, 0.4), (1, 0.8, 0.4), (2, 0.8, 0.4), (0, 0.0, 0.6), (1, 0.9, 0.3), (2, 0.975, 0.2), (1, 1.0, 0.9)]
    for c, x in zip(cfg, run(7, 10, 10, cfg)): print(c, repr(x))
