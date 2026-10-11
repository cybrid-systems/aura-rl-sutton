# Chapter 8 — Planning and Learning with Tabular Methods

Status: done.

| Driver | Book | What it does |
|---|---|---|
| `dyna_maze.aura` | Example 8.1, Figure 8.2 | Dyna-Q on the 6×9 Dyna maze with n ∈ {0, 5, 50} planning steps (α = 0.1, ε = 0.1, γ = 0.95): steps per episode over 50 episodes, mean over runs |
| `changing_maze.aura` | Examples 8.2–8.3, Figures 8.4–8.5 | Dyna-Q vs Dyna-Q+ (n = 10, α = 1.0, ε = 0.1, γ = 0.95) on the blocking maze (right gap closes and left gap opens at step 1000, 3000 steps; κ = 1e-4) and the shortcut maze (right shortcut opens at step 3000, 6000 steps; κ = 1e-3): cumulative reward, mean over runs |
| `prioritized_sweeping.aura` | Sec 8.4, Example 8.4 | prioritized sweeping vs Dyna-Q on the Dyna maze at resolutions 1–3 (47 / 188 / 423 free cells): Q updates until the greedy path is within 1.2 × the shortest path |
| `expected_vs_sample.aura` | Sec 8.5, Figure 8.7 | RMS error of sample updates after t one-successor computations for b = 2, 10, 100, 1000, next to √((b−1)/(bt)); an expected update reaches error 0 after b computations |
| `trajectory_sampling.aura` | Sec 8.6, Figure 8.8 | random tasks with 1000 states, b = 1 and 3: value of the start state under the greedy policy, on-policy trajectory sampling vs uniform sweeps of expected updates |

Code: `lib/envs/maze.aura` (mazes; `maze-switch!` installs the second wall layout; `maze-scale`
builds the k× resolution maze of Example 8.4 with a k×k goal block), `lib/algos/dyna.aura`
(Dyna-Q / Dyna-Q+), `lib/algos/prioritized.aura` (prioritized sweeping) and
`lib/algos/sample-updates.aura` (Figures 8.7 and 8.8).

**Dyna-Q / Dyna-Q+.** The model keeps, per observed state, the list of actions tried there and
the last (s', r, time) of each; planning picks a random observed state, then a random action
tried in it. Dyna-Q+ adds κ√τ to the planning reward (τ = real steps since the pair was last
tried) and, when a state is first observed, enters its untried actions as "stay in place,
reward 0, last tried at time 1". Planning draws from its own Park–Miller generator, so acting
draws the same random numbers for every n: with Q = 0 and zero reward until the goal, the first
episode is identical for every number of planning steps.

**Prioritized sweeping** follows the boxed algorithm for deterministic environments: every real
step updates the model and queues (S, A) if its priority exceeds θ = 1e-4; up to n = 5 planning
updates pop the highest priority pair, update it (α = 0.5) and queue every predicted predecessor
of S above θ. There is no direct update from the real transition. The queue is a binary max-heap
with lazy deletion; re-inserting a pair keeps the higher priority. Dyna-Q uses the same n, α, ε
and is charged n + 1 updates per real step.

**Figure 8.8.** Each (s, a) has b fixed random successors (equally likely) with a fixed N(0, 1)
reward each, and every transition ends the episode with probability 0.1. The expected update is
Q(s, a) ← 0.9 · mean_k [r + max_a' Q(s_k, a')]. Uniform cycles through all (s, a); on-policy
follows ε-greedy (ε = 0.1) episodes from state 0. The start-state value of the greedy policy is
computed by iterative policy evaluation to 1e-4 (warm-started), not by Monte Carlo episodes.

## Results (seed 2026, `3034d4723` RelWithDebInfo)

Example 8.4, 2 runs (3 min). Q updates until the greedy path is near-optimal:

| resolution | free cells | prioritized sweeping | Dyna-Q | ratio |
|---|---|---|---|---|
| 1 | 47 | 1 133 | 10 455 | 9.2 |
| 2 | 188 | 7 198 | 14 082 | 2.0 |
| 3 | 423 | 21 903 | 54 873 | 2.5 |

Prioritized sweeping needs 2–9 times fewer updates (book: about 5–10 times, growing with the
maze). Two runs leave the Dyna-Q column noisy.

Figure 8.7, 100 runs (13 s). Measured RMS / √((b−1)/(bt)):

| b | t = b/10 | t = b/2 | t = b | t = 2b |
|---|---|---|---|---|
| 2 | 0.689 / 0.707 (t = 1) | — | 0.471 / 0.500 | 0.370 / 0.354 |
| 10 | 0.916 / 0.949 | 0.426 / 0.424 | 0.334 / 0.300 | 0.222 / 0.212 |
| 100 | 0.302 / 0.315 | 0.148 / 0.141 | 0.102 / 0.099 | 0.066 / 0.070 |
| 1000 | 0.102 / 0.100 | 0.039 / 0.045 | 0.029 / 0.032 | 0.023 / 0.022 |

For large b a fraction of b sample updates already removes most of the error, while an expected
update has done nothing useful until all b computations are finished.

Figure 8.8, 1000 states, 2 tasks, 6000 updates (4 min). Start-state value:

| updates | 0 | 500 | 1000 | 1500 | 2000 | 3000 | 4000 | 6000 |
|---|---|---|---|---|---|---|---|---|
| b = 1 on-policy | 2.04 | 6.51 | 6.51 | 6.51 | 6.51 | 6.51 | 6.51 | 6.51 |
| b = 1 uniform | 2.04 | 4.28 | 4.14 | 6.60 | 7.47 | 6.92 | 7.01 | 8.04 |
| b = 3 on-policy | −0.57 | 1.62 | 1.93 | 2.18 | 2.33 | 2.48 | 2.56 | 2.67 |
| b = 3 uniform | −0.57 | 0.78 | 1.50 | 2.42 | 3.09 | 3.14 | 3.19 | 3.23 |

As in the book, on-policy sampling is far ahead early (after 500 updates: 6.51 vs 4.28 for
b = 1, 1.62 vs 0.78 for b = 3) and the uniform sweeps overtake it after about one sweep (2000
updates) and end higher. The 10 000-state and b = 10 curves are available with
`RL_STATES=10000` / `RL_BRANCHES=3`, but take much longer on the Soft interpreter.

Checks (`tests/test_ch08_dyna.aura`, `tests/test_ch08_planning.aura`):

- Maze dynamics: walls and edges block, the goal pays 1 and ends the episode, and the
  blocking / shortcut mazes change as in the book. The 2× maze has its start, walls and goal
  block in the right cells.
- The Dyna-Q model knows only tried actions; the Dyna-Q+ model also knows the untried
  actions of an observed state as stay-in-place with reward 0.
- Figure 8.2 (1 run × 15 episodes): the first episode is identical for n = 0 and n = 10;
  in episodes 6–15, n = 10 needs less than a third of the steps of n = 0 and stays within
  14–25 steps (optimum 14).
- Figure 8.4 (1 run × 2000 steps): both methods reach the goal more than 30 times before the
  change; Dyna-Q stalls right after it; Dyna-Q+ gains at least as much as Dyna-Q after it.
- Priority queue: pops in priority order, keeps the higher of two inserts of the same pair,
  skips stale entries, and grows past its initial 64 slots.
- Example 8.4 at resolution 1: prioritized sweeping needs less than half the updates of Dyna-Q.
- Figure 8.7, b = 10, 400 runs: RMS at t = 1, b, 2b within tolerance of √((b−1)/(bt)).
- Figure 8.8, 200 states, b = 3: both methods start from the same value and improve it.

Run sizes (defaults): Figure 8.2 with 2 runs (book 30), Figures 8.4–8.5 with 3 runs (book 20
and 5), Example 8.4 with 2 runs up to resolution 3, Figure 8.8 with 2 tasks (book 200).
Knobs: `RL_RUNS`, `RL_EPISODES` (Figure 8.2), `RL_MAZE` (`both` / `blocking` / `shortcut`),
`RL_MAXRES` (Example 8.4), `RL_STATES` / `RL_BRANCHES` / `RL_UPDATES` / `RL_EVERY` / `RL_TASKS`
(Figure 8.8), `RL_SEED`.

Reference implementation (Python, for cross-checking numbers only): `chapter08/maze.py`,
`expectation_vs_sample.py` and `trajectory_sampling.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction)
(its κ, α and n for Figures 8.4–8.5 and its Example 8.4 settings are used here; the book does
not list them). Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 8`
