# Chapter 10 — On-policy Control with Approximation

Status: partial (mountain car, Fig 10.1–10.3); Fig 10.4 (α × n sweep) and differential semi-gradient Sarsa on
access control (Fig 10.5) TODO

| Driver | Book | What it does |
|---|---|---|
| `mountain_car_sarsa.aura` | Example 10.1, Fig 10.1, Fig 10.2 | episodic semi-gradient Sarsa with 8 tilings; cost-to-go −max_a q after the first and the last episode; steps per episode for α = 0.1/8, 0.2/8, 0.5/8 |
| `mountain_car_nstep.aura` | Fig 10.3 | semi-gradient n-step Sarsa, n = 1 (α = 0.5/8) vs n = 8 (α = 0.3/8) |

Library code: `lib/envs/mountain-car.aura` (dynamics), `lib/algos/semigrad-sarsa.aura` (tile coder and n-step Sarsa).
Tests: `tests/test_ch10_mountain_car.aura`.

Tile coding: 8 tilings of an 8 × 8 grid over (position, velocity), tiling k offset by (k, 3k) eighths of a tile, one
extra row and column, a separate weight block per action: 8 × 11 × 11 × 3 = 2 904 weights. This is the book's
tile coder without the hashing (no collisions). Actions are greedy with random ties; zero initial weights are
optimistic because every reward is −1.

Reference implementation (Python, for cross-checking numbers only): `chapter10/mountain_car.py, access_control.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 10`
