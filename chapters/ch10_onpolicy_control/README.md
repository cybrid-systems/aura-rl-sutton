# Chapter 10 — On-policy Control with Approximation

Status: done (mountain car Fig 10.1–10.4, access control Fig 10.5)

| Driver | Book | What it does |
|---|---|---|
| `mountain_car_sarsa.aura` | Example 10.1, Fig 10.1, Fig 10.2 | episodic semi-gradient Sarsa with 8 tilings; cost-to-go −max_a q after the first and the last episode; steps per episode for α = 0.1/8, 0.2/8, 0.5/8 |
| `mountain_car_nstep.aura` | Fig 10.3 | semi-gradient n-step Sarsa, n = 1 (α = 0.5/8) vs n = 8 (α = 0.3/8) |
| `mountain_car_sweep.aura` | Fig 10.4 | n-step Sarsa, mean steps per episode over the first 20 episodes for n = 1, 2, 4, 8, 16 × α = 0.2, 0.5, 0.9 (/8); 1 run by default (book: first 50 episodes, 100 runs), so single cells are noisy (`RL_RUNS`, `RL_NS`, `RL_ALPHAS`) |
| `access_control.aura` | Example 10.2, Fig 10.5 | differential semi-gradient Sarsa (α = β = 0.01, ε = 0.1) on the 10-server access-control queue; prints the learned R̄, the greedy policy and max_a q per (priority, free servers); 400 000 steps by default (book 2 000 000) |

Library code: `lib/envs/mountain-car.aura` (dynamics), `lib/algos/semigrad-sarsa.aura` (tile coder and n-step Sarsa),
`lib/algos/diff-sarsa.aura` (access-control task and differential Sarsa).
Tests: `tests/test_ch10_mountain_car.aura`, `tests/test_ch10_access_control.aura`.

Tile coding: 8 tilings of an 8 × 8 grid over (position, velocity), tiling k offset by (k, 3k) eighths of a tile, one
extra row and column, a separate weight block per action: 8 × 11 × 11 × 3 = 2 904 weights. This is the book's
tile coder without the hashing (no collisions). Actions are greedy with random ties; zero initial weights are
optimistic because every reward is −1.

Access control: the state (free servers 0–10, priority 1/2/4/8) is one-hot, so q is a 11 × 4 × 2 table. After the
action, each busy server frees with probability 0.06. With no free server the customer is rejected. The optimal
average reward is 2.748 (relative value iteration, `tests/oracle/access_control_rvi.py`). The optimal policy never
accepts priority 1, accepts priority 2 with at least 4 free servers, and accepts 4 and 8 whenever a server is free.
At the default 400 000 steps the learned R̄ is 2.73 and the greedy policy matches the optimal one except in the
rarely visited columns with 8–10 free servers (the book's Figure 10.5 has the same ragged right edge).

Reference implementation (Python, for cross-checking numbers only): `chapter10/mountain_car.py, access_control.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 10`
