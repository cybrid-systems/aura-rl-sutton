#!/usr/bin/env python3
"""Independent Python check of lib/algos/policy-gradient.aura (Chapter 13).

Short corridor with switched actions (Example 13.1), softmax policy with
pi(right) clipped to [0.05, 0.95], gamma = 1. Replays the same Park-Miller PRNG
as lib/rl/rng.aura, so a seed gives the same episodes and parameters as the Aura
code. Prints theta / baseline / critic and the mean return after a fixed number of
episodes for REINFORCE, REINFORCE with baseline and one-step actor-critic, plus
the exact optimum of Exercise 13.1. Used to set the expected values in
tests/test_ch13_policy_gradient.aura.
"""
import math

M = 2147483647
EPS = 0.05


class Rng:
    def __init__(self, s): self.s = 1 + s % (M - 1)
    def next(self): self.s = (16807 * self.s) % M; return self.s
    def uniform(self): return (1.0 * self.next()) / (1.0 * M)


def step(s, a):
    if s == 0: return 1 if a == 1 else 0
    if s == 1: return 0 if a == 1 else 2
    return 3 if a == 1 else 1


class Agent:
    def __init__(self, t0, t1):
        self.th = [t0, t1]; self.w = 0.0; self.v = [0.0] * 4

    def p(self):
        p = 1.0 / (1.0 + math.exp(self.th[1] - self.th[0]))
        return EPS if p < EPS else (1.0 - EPS if p > 1.0 - EPS else p)

    def act(self, rng): return 1 if rng.uniform() < self.p() else 0

    def grad_step(self, a, c):
        p = self.p(); g0 = (1.0 - p) if a == 1 else (0.0 - p)
        self.th[0] += c * g0; self.th[1] -= c * g0

    def gen(self, rng):
        s, acts = 0, []
        while s != 3:
            a = self.act(rng); acts.append(a); s = step(s, a)
        return acts

    def reinforce(self, rng, alpha):
        acts = self.gen(rng); T = len(acts)
        for t, a in enumerate(acts): self.grad_step(a, alpha * (-1.0 * (T - t)))
        return -1.0 * T

    def reinforce_baseline(self, rng, alpha, aw):
        acts = self.gen(rng); T = len(acts)
        for t, a in enumerate(acts):
            delta = (-1.0 * (T - t)) - self.w
            self.w += aw * delta
            self.grad_step(a, alpha * delta)
        return -1.0 * T

    def actor_critic(self, rng, alpha, aw):
        s, t = 0, 0
        while s != 3:
            a = self.act(rng); s2 = step(s, a)
            delta = (-1.0 + self.v[s2]) - self.v[s]
            self.v[s] += aw * delta
            self.grad_step(a, alpha * delta)
            s, t = s2, t + 1
        return -1.0 * t


def run(method, seed, episodes, alpha, aw=0.0):
    rng = Rng(seed); ag = Agent(-1.47, 1.47); tot = 0.0
    for _ in range(episodes):
        if method == 0: tot += ag.reinforce(rng, alpha)
        elif method == 1: tot += ag.reinforce_baseline(rng, alpha, aw)
        else: tot += ag.actor_critic(rng, alpha, aw)
    return ag, tot / episodes


def true_value(p): return (2 * p - 4) / (p * (1 - p))


if __name__ == "__main__":
    pstar = 2 - math.sqrt(2)
    print("p* = %.10f  v* = %.10f  v(0.5) = %.10f  v(0.05) = %.10f" % (pstar, true_value(pstar), true_value(0.5), true_value(0.05)))
    for name, m, a, aw in (("REINFORCE a=2^-13", 0, 2 ** -13, 0.0),
                           ("REINFORCE a=2^-12", 0, 2 ** -12, 0.0),
                           ("baseline a=2^-9 aw=2^-6", 1, 2 ** -9, 2 ** -6),
                           ("actor-critic a=2^-6 aw=2^-4", 2, 2 ** -6, 2 ** -4)):
        ag, mean = run(m, 7, 200, a, aw)
        print("%-28s seed 7, 200 episodes: theta = (%.10f, %.10f) w = %.10f v = (%.10f, %.10f, %.10f) p = %.10f mean return = %.6f"
              % (name, ag.th[0], ag.th[1], ag.w, ag.v[0], ag.v[1], ag.v[2], ag.p(), mean))
