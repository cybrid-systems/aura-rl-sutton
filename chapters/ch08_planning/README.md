# Chapter 8 — Planning and Learning with Tabular Methods

Status: partial. Dyna-Q (Sec 8.2, Example 8.1 / Figure 8.2) and Dyna-Q+ on the blocking
and shortcut mazes (Sec 8.3, Examples 8.2–8.3 / Figures 8.4–8.5) are done. Prioritized
sweeping (Sec 8.4), expected vs sample updates (Figure 8.7) and trajectory sampling
(Figure 8.8) are TODO.

| Driver | Book | What it does |
|---|---|---|
| `dyna_maze.aura` | Example 8.1, Figure 8.2 | Dyna-Q on the 6×9 Dyna maze with n ∈ {0, 5, 50} planning steps (α = 0.1, ε = 0.1, γ = 0.95): steps per episode over 50 episodes, mean over runs |
| `changing_maze.aura` | Examples 8.2–8.3, Figures 8.4–8.5 | Dyna-Q vs Dyna-Q+ (n = 10, α = 1.0, ε = 0.1, γ = 0.95) on the blocking maze (right gap closes and left gap opens at step 1000, 3000 steps; κ = 1e-4) and the shortcut maze (right shortcut opens at step 3000, 6000 steps; κ = 1e-3): cumulative reward, mean over runs |

Code: `lib/envs/maze.aura` (mazes, `maze-switch!` installs the second wall layout) and
`lib/algos/dyna.aura`. The model keeps, per observed state, the list of actions tried there
and the last (s', r, time) of each; planning picks a random observed state, then a random
action tried in it. Dyna-Q+ adds κ√τ to the planning reward (τ = real steps since the pair
was last tried) and, when a state is first observed, enters its untried actions as
"stay in place, reward 0, last tried at time 1". Planning draws from its own Park–Miller
generator, so acting draws the same random numbers for every n: with Q = 0 and zero
reward until the goal, the first episode is identical for every number of planning steps.

Checks (`tests/test_ch08_dyna.aura`):

- Maze dynamics: walls and edges block, the goal pays 1 and ends the episode, and the
  blocking / shortcut mazes change as in the book.
- The Dyna-Q model knows only tried actions; the Dyna-Q+ model also knows the untried
  actions of an observed state as stay-in-place with reward 0.
- Figure 8.2 (1 run × 15 episodes): the first episode is identical for n = 0 and n = 10;
  in episodes 6–15, n = 10 needs less than a third of the steps of n = 0 and stays within
  14–25 steps (optimum 14).
- Figure 8.4 (1 run × 2000 steps): both methods reach the goal more than 30 times before the
  change; Dyna-Q stalls right after it (fewer goals in steps 1001–1200 than in 801–1000);
  Dyna-Q+ gains at least as much as Dyna-Q after the change.

Run sizes (defaults): Figure 8.2 with 2 runs (book 30), Figures 8.4–8.5 with 3 runs (book 20
and 5). Knobs: `RL_RUNS`, `RL_EPISODES` (Figure 8.2), `RL_MAZE` (`both` / `blocking` /
`shortcut`), `RL_SEED`.

Reference implementation (Python, for cross-checking numbers only): `chapter08/maze.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction)
(its κ, α and n for Figures 8.4–8.5 are used here; the book does not list them).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 8`
