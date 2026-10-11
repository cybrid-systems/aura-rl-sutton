# Chapter 7 — n-step Bootstrapping

Status: done. n-step TD prediction (Sec 7.1, Example 7.1 / Figure 7.2), n-step Sarsa
(Sec 7.2), n-step Expected Sarsa (Sec 7.2), off-policy n-step Sarsa with importance
sampling (Sec 7.3), n-step Tree Backup (Sec 7.5) and off-policy n-step Q(σ) (Sec 7.6).

| Driver | Book | What it does |
|---|---|---|
| `nstep_td_random_walk.aura` | Example 7.1, Figure 7.2 | n-step TD on the 19-state random walk (left terminal −1, right +1, V₀ = 0), n ∈ {1, 2, 4, 8, 16} × α ∈ {0.1 … 1.0}: RMS error over the 19 states, averaged over the first 10 episodes and over runs |
| `nstep_control_cliff.aura` | Sec 7.2, 7.5 | n-step Sarsa, n-step Expected Sarsa and n-step Tree Backup on cliff walking (ε = 0.1, γ = 1), n ∈ {1, 2, 4, 8}: online reward per episode over the second half of training, greedy path length |
| `nstep_offpolicy_cliff.aura` | Sec 7.3, 7.6 | off-policy n-step Sarsa with importance sampling (n ∈ {1, 2, 4, 8}) and off-policy n-step Q(σ) (n = 4, σ ∈ {0, 0.5, 1, random}) on cliff walking; behaviour ε_b-greedy (ε_b = 0.1), greedy target; online reward under b and return of the greedy target policy |

Code: `lib/algos/nstep.aura`. S / A / R are ring buffers of length n+1 indexed `t mod (n+1)`,
which is exactly the history an update at τ = t − n + 1 reads. Tree Backup uses the greedy
target policy (ties split evenly) and needs no importance sampling.

Off-policy (`ns-off-episode!`): behaviour b is ε_b-greedy and target π is ε_π-greedy
w.r.t. the current Q (ε_π = 0 is greedy). As in the book's Q(σ) box, the ratio
ρ_t = π(A_t|S_t) / b(A_t|S_t) is computed and stored when A_t is chosen, so π and b see the
same Q; π(A_k|S_k) and V̄(S_k) inside the Q(σ) recursion (7.17) use the Q at update time.
IS n-step Sarsa multiplies the update by ρ_{τ+1:min(τ+n, T−1)}. σ is a constant in [0, 1] or
`'rand` (σ_t ~ Bernoulli(0.5), drawn and stored per step).

Checks (`tests/test_ch07_nstep.aura`):

- With n = 1 and the same seed, n-step Sarsa, n-step Expected Sarsa and Tree Backup give
  bit-identical Q tables to one-step Sarsa, Expected Sarsa and Q-learning from `lib/algos/td.aura`.
- n larger than any episode with α = 1 is Monte Carlo: every visited state takes the return (±1).
- Figure 7.2 shape: n = 4 beats n = 1 at α = 0.4; n = 16 with α = 1 is worse.
- Cliff walking: 2-step Sarsa scores better online than 2-step Tree Backup, which learns
  the near-edge greedy path.

Off-policy checks (`tests/test_ch07_offpolicy.aura`), all to 1e-9 with the same seed:

- IS n-step Sarsa with ε_π = ε_b (ρ = 1 exactly) equals one-step Sarsa (n = 1) and on-policy
  3-step Sarsa (n = 3).
- Q(σ = 0) with a greedy target equals Q-learning (n = 1) and 3-step Tree Backup (n = 3).
- Q(σ = 1), n = 1, ε_π = ε_b equals one-step Expected Sarsa.
- ε-greedy probabilities sum to 1 and split ties; a greedy target gives 0 to non-maximal actions.

Run sizes (defaults): random walk 10 runs (book 100), n up to 16 (book up to 512);
cliff walking 3 runs × 200 episodes at α = 0.2 (on- and off-policy). Knobs: `RL_RUNS`, `RL_EPISODES`, `RL_ALPHA`,
`RL_SEED`.

Reference implementation (Python, for cross-checking numbers only): `chapter07/random_walk.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 7`
