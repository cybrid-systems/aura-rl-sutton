# Chapter 6 — Temporal-Difference Learning

Status: done for Example 6.2 (TD(0) vs MC), Figure 6.2 (batch updating), 6.5 (windy
gridworld), 6.6 (cliff walking, including Expected Sarsa), Figure 6.3 (interim / asymptotic
performance vs α) and 6.7 (maximization bias / Double Q-learning).

| Driver | Book | What it does |
|---|---|---|
| `random_walk.aura` | Example 6.2 | TD(0) estimates after 0/1/10/100 episodes; RMS error curves for TD(0) α ∈ {0.05, 0.1, 0.15} and constant-α MC α ∈ {0.01 … 0.04}, 100 runs |
| `batch_updating.aura` | Figure 6.2 | batch TD(0) vs batch constant-α MC (α = 0.001): after each episode, replay all episodes so far until Σ\|ΔV\| < 1e-3; RMS error per episode |
| `windy_gridworld.aura` | Example 6.5 | Sarsa (ε = 0.1, α = 0.5): episodes finished per 1 000 steps, greedy path length (optimal 15) |
| `cliff_walking.aura` | Example 6.6 | Sarsa vs Q-learning vs Expected Sarsa: sum of rewards per episode in blocks of 50, greedy paths |
| `expected_sarsa_sweep.aura` | Figure 6.3 | Sarsa / Expected Sarsa / Q-learning on cliff walking for α ∈ {0.1, 0.3, 0.5, 0.7, 0.9, 1.0}: interim (first 100 episodes) and asymptotic (longer run) mean reward per episode |
| `maximization_bias.aura` | Example 6.7 | % of `left` actions from A for Q-learning vs Double Q-learning |

Code: `lib/algos/td.aura` (TD(0), constant-α MC, Sarsa / Q-learning / Expected Sarsa on any
`(step s a) → (s' r done?)` env, Double Q-learning), `lib/algos/td-batch.aura` (batch
TD / MC; stored episodes are kept as transition / visit counts, which gives the same sums as
replaying every trajectory), envs `lib/envs/random-walk.aura`,
`lib/envs/windy.aura`, `lib/envs/cliffwalking.aura`.

Run sizes (defaults): random walk 100 runs (as in the book); batch updating 20 runs × 100
episodes (book: 100 runs); α sweep 4 runs × 100 episodes interim, 1 run × 500 episodes
asymptotic (book: 50 000 runs × 100 and 10 runs × 100 000; knobs `RL_ASYM_RUNS`,
`RL_ASYM_EPISODES`); cliff walking 10 runs × 500
episodes (book: 50 runs); maximization bias 200 runs × 300 episodes (book: 10 000 runs).
Knobs: `RL_RUNS`, `RL_EPISODES`, `RL_SEED`.

Results at the defaults (Aura `2f815c188`, seed 2026) are in the top-level README.
Tests: `tests/test_ch06_td.aura`, `tests/test_ch06_batch_sweep.aura`.

Reference implementation (Python, for cross-checking numbers only): `chapter06/random_walk.py` (also batch updating), `windy_grid_world.py`, cliff_walking.py, maximization_bias.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 6`
