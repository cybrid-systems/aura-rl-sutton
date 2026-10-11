# Chapter 11 — Off-policy Methods with Approximation

Status: done (Baird's counterexample: Fig 11.2, 11.6, 11.7)

| Driver | Book | What it does |
|---|---|---|
| `baird.aura` | Example 11.1, Fig 11.2 (left / right), Fig 11.6 (left / right), Fig 11.7 | semi-gradient off-policy TD(0) and semi-gradient DP diverge (α = 0.01); TDC (α = 0.005, β = 0.05), sample and expected, drives √PBE towards 0 while √VE stays near 1.9; expected emphatic TD (α = 0.03) drives √VE to 0. Prints w₁, w₆, w₇, w₈, √VE and √PBE every 100 steps |

Library code: `lib/envs/baird.aura` (states, features, behaviour policy), `lib/algos/offpolicy-approx.aura`
(semi-gradient TD, semi-gradient DP, TDC, expected TDC, expected emphatic TD, VE / PBE).
Tests: `tests/test_ch11_baird.aura`. The expected sweeps are deterministic and match an independent numpy version
(`tests/oracle/baird_expected.py`) to 6 digits.

Notes:

- μ is uniform over the 7 states (the behaviour policy's stationary distribution). All true values are 0, so
  √VE = √(mean v(s)²).
- The 7 × 8 feature matrix has rank 7, so the projection onto the representable functions is the identity and
  PBE = BE on this problem. √PBE is computed from the expected TD error δ̄(s) = γ v(lower) − v(s) (only the solid
  action has ρ ≠ 0, and b(solid) · ρ(solid) = 1).
- Expected updates are synchronous: every sweep uses the weights from the start of the sweep.
- Expected emphatic TD keeps an expected emphasis M (interest 1, λ = 0). M converges to 1 / (1 − γ) = 100, and the
  weights to (22/13, …, 22/13, 88/13, −44/13), where every value is 0.

Reference implementation (Python, for cross-checking numbers only): `chapter11/counterexample.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 11`
