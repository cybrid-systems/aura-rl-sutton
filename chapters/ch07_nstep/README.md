# Chapter 7 — n-step Bootstrapping

Status: done for n-step TD prediction (Sec 7.1, Example 7.1 / Figure 7.2), n-step Sarsa
(Sec 7.2), n-step Expected Sarsa (Sec 7.2) and n-step Tree Backup (Sec 7.5). Off-policy
n-step Sarsa with importance sampling (Sec 7.3) and n-step Q(σ) (Sec 7.6) are TODO.

| Driver | Book | What it does |
|---|---|---|
| `nstep_td_random_walk.aura` | Example 7.1, Figure 7.2 | n-step TD on the 19-state random walk (left terminal −1, right +1, V₀ = 0), n ∈ {1, 2, 4, 8, 16} × α ∈ {0.1 … 1.0}: RMS error over the 19 states, averaged over the first 10 episodes and over runs |
| `nstep_control_cliff.aura` | Sec 7.2, 7.5 | n-step Sarsa, n-step Expected Sarsa and n-step Tree Backup on cliff walking (ε = 0.1, γ = 1), n ∈ {1, 2, 4, 8}: online reward per episode over the second half of training, greedy path length |

Code: `lib/algos/nstep.aura`. S / A / R are ring buffers of length n+1 indexed `t mod (n+1)`,
which is exactly the history an update at τ = t − n + 1 reads. Tree Backup uses the greedy
target policy (ties split evenly) and needs no importance sampling.

Checks (`tests/test_ch07_nstep.aura`):

- With n = 1 and the same seed, n-step Sarsa, n-step Expected Sarsa and Tree Backup give
  bit-identical Q tables to one-step Sarsa, Expected Sarsa and Q-learning from `lib/algos/td.aura`.
- n larger than any episode with α = 1 is Monte Carlo: every visited state takes the return (±1).
- Figure 7.2 shape: n = 4 beats n = 1 at α = 0.4; n = 16 with α = 1 is worse.
- Cliff walking: 2-step Sarsa scores better online than 2-step Tree Backup, which learns
  the near-edge greedy path.

Run sizes (defaults): random walk 10 runs (book 100), n up to 16 (book up to 512);
cliff walking 3 runs × 200 episodes at α = 0.2. Knobs: `RL_RUNS`, `RL_EPISODES`, `RL_ALPHA`,
`RL_SEED`.

Reference implementation (Python, for cross-checking numbers only): `chapter07/random_walk.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 7`
