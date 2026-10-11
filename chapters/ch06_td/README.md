# Chapter 6 — Temporal-Difference Learning

Status: done for Example 6.2 (TD(0) vs MC), 6.5 (windy gridworld), 6.6 (cliff walking,
including Expected Sarsa) and 6.7 (maximization bias / Double Q-learning). Batch updating
(Fig 6.2) and the Expected Sarsa α sweep (Fig 6.3) are TODO.

| Driver | Book | What it does |
|---|---|---|
| `random_walk.aura` | Example 6.2 | TD(0) estimates after 0/1/10/100 episodes; RMS error curves for TD(0) α ∈ {0.05, 0.1, 0.15} and constant-α MC α ∈ {0.01 … 0.04}, 100 runs |
| `windy_gridworld.aura` | Example 6.5 | Sarsa (ε = 0.1, α = 0.5): episodes finished per 1 000 steps, greedy path length (optimal 15) |
| `cliff_walking.aura` | Example 6.6 | Sarsa vs Q-learning vs Expected Sarsa: sum of rewards per episode in blocks of 50, greedy paths |
| `maximization_bias.aura` | Example 6.7 | % of `left` actions from A for Q-learning vs Double Q-learning |

Code: `lib/algos/td.aura` (TD(0), constant-α MC, Sarsa / Q-learning / Expected Sarsa on any
`(step s a) → (s' r done?)` env, Double Q-learning), envs `lib/envs/random-walk.aura`,
`lib/envs/windy.aura`, `lib/envs/cliffwalking.aura`.

Run sizes (defaults): random walk 100 runs (as in the book); cliff walking 10 runs × 500
episodes (book: 50 runs); maximization bias 200 runs × 300 episodes (book: 10 000 runs).
Knobs: `RL_RUNS`, `RL_EPISODES`, `RL_SEED`.

Results at the defaults (Aura `2f815c188`, seed 2026) are in the top-level README.
Tests: `tests/test_ch06_td.aura`.

Reference implementation (Python, for cross-checking numbers only): `chapter06/random_walk.py, windy_grid_world.py, cliff_walking.py, maximization_bias.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 6`
