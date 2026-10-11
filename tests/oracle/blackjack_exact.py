#!/usr/bin/env python3
"""Exact blackjack values for the rules in lib/envs/blackjack.aura (infinite deck,
dealer sticks on 17+, no natural bonus). Used only to produce oracle constants for
tests/test_ch05_mc.aura; prints them as Aura-readable lines."""
from functools import lru_cache

CARDS = [(c, (4 if c == 10 else 1) / 13) for c in range(1, 11)]

def add(s, u, c):
    eleven = c == 1 and s + 11 <= 21
    s2 = s + (11 if eleven else c)
    u2 = u or eleven
    if s2 > 21 and u2:
        return s2 - 10, False
    return s2, u2

@lru_cache(None)
def dealer_dist(s, u):
    """distribution of final dealer sum (22 = bust) from (s, u)"""
    if s >= 17:
        return {min(s, 22): 1.0}
    out = {}
    for c, p in CARDS:
        s2, u2 = add(s, u, c)
        for k, q in dealer_dist(s2, u2).items():
            out[k] = out.get(k, 0) + p * q
    return out

def dealer_from_show(show):
    s, u = add(0, False, show)
    out = {}
    for c, p in CARDS:
        s2, u2 = add(s, u, c)
        for k, q in dealer_dist(s2, u2).items():
            out[k] = out.get(k, 0) + p * q
    return out

def stick_value(ps, show):
    r = 0.0
    for d, p in dealer_from_show(show).items():
        r += p * (1 if d > 21 or ps > d else 0 if ps == d else -1)
    return r

def make_v(policy):
    @lru_cache(None)
    def v(s, u, show):
        if policy(s, u, show) == "stick":
            return stick_value(s, show)
        r = 0.0
        for c, p in CARDS:
            s2, u2 = add(s, u, c)
            r += p * (-1 if s2 > 21 else v(s2, u2, show))
        return r
    return v

@lru_cache(None)
def vstar(s, u, show):
    return max(qstar(s, u, show))

@lru_cache(None)
def qstar(s, u, show):
    hit = 0.0
    for c, p in CARDS:
        s2, u2 = add(s, u, c)
        hit += p * (-1 if s2 > 21 else vstar(s2, u2, show))
    return (stick_value(s, show), hit)

v20 = make_v(lambda s, u, d: "stick" if s >= 20 else "hit")
print("; v_pi stick-20, index ((u*10)+(sum-12))*10+(show-1)")
print("(define bj-exact-v20 (vector", " ".join("%.5f" % v20(s, u, d) for u in (False, True) for s in range(12, 22) for d in range(1, 11)), "))")
print("(define bj-exact-vstar (vector", " ".join("%.5f" % vstar(s, u, d) for u in (False, True) for s in range(12, 22) for d in range(1, 11)), "))")
print("; optimal action: 1 = hit, 0 = stick")
print("(define bj-exact-pistar (vector", " ".join(str(int(qstar(s, u, d)[1] > qstar(s, u, d)[0])) for u in (False, True) for s in range(12, 22) for d in range(1, 11)), "))")
print("; Fig 5.3 state (13, usable, show 2) under stick-20:", "%.5f" % v20(13, True, 2))
# average return of whole game under stick-20 (deal until >=12)
@lru_cache(None)
def deal(s, u):
    if s >= 12: return {(s, u): 1.0}
    out = {}
    for c, p in CARDS:
        for k, q in deal(*add(s, u, c)).items(): out[k] = out.get(k, 0) + p * q
    return out
g = sum(p * pc * v20(s, u, show) for (s, u), p in deal(0, False).items() for show, pc in CARDS)
gs = sum(p * pc * vstar(s, u, show) for (s, u), p in deal(0, False).items() for show, pc in CARDS)
print("; mean return stick-20 = %.5f, optimal = %.5f" % (g, gs))
