# Chapter 13 — Policy Gradient Methods

Status: done (short corridor, Fig 13.1 / 13.2, one-step actor-critic)

| Driver | Book | What it does |
|---|---|---|
| `short_corridor.aura` | Example 13.1, Fig 13.1, 13.2, Sec 13.5 | REINFORCE for α = 2^-12, 2^-13, 2^-14; REINFORCE with baseline (α_θ = 2^-9, α_w = 2^-6); one-step actor-critic (α_θ = 2^-6, α_w = 2^-4); total reward per episode averaged over runs, in blocks of episodes, plus the mean final π(right); 20 runs × 1000 episodes by default (book 100 runs), about 4 min with a RelWithDebInfo build |

Library code: `lib/envs/short-corridor.aura` (Example 13.1 and the exact value of Exercise 13.1),
`lib/algos/policy-gradient.aura` (the three methods). Tests: `tests/test_ch13_policy_gradient.aura`.

Notes:

- Every state looks the same to the policy: x(s, right) = (1, 0), x(s, left) = (0, 1), softmax in θ·x, so
  π(right) = 1 / (1 + exp(θ_left − θ_right)) in all three states. All runs start at θ = (−1.47, 1.47), π(right) = 0.05.
- As in the book's figures, the policy is kept at least ε = 0.05 stochastic: π(right) is clipped to [0.05, 0.95],
  and the clipped value is used in ∇ln π as well.
- γ = 1, so the γ^t factors are 1. REINFORCE updates θ in place after the episode, t = 0 … T−1, with
  G_t = −(T − t). The baseline is a single state-independent weight w (the states are indistinguishable).
- The actor-critic is not in the book's figures. It uses a tabular critic v(s) over the three states, so δ is
  not always −1, unlike a critic that sees the policy's features.
- Exact value: v(0) = (2p − 4) / (p (1 − p)) for π(right) = p, maximised at p* = 2 − √2 = 0.586, v* = −11.657.
- `tests/oracle/short_corridor.py` reimplements the corridor and the three methods with the same Park–Miller PRNG.
  With seed 7 and 200 episodes it gives the same θ, w, critic and mean return; the test checks them to 1e-7.
- Step sizes are written as literals (`0.0001220703125` for 2^-13): `(expt 2.0 -13)` never returns on this Aura
  ([#4458](https://github.com/cybrid-systems/aura/issues/4458)).

Result at the defaults (Aura `3034d4723`, RelWithDebInfo, seed 2026, 20 runs; mean total reward per episode):

| Method | 1–10 | 11–50 | 51–100 | 101–200 | 201–500 | 501–1000 | final π(right) |
|---|---|---|---|---|---|---|---|
| REINFORCE, α = 2^-12 | −65.8 | −43.9 | −24.3 | −16.8 | −13.3 | −11.9 | 0.566 |
| REINFORCE, α = 2^-13 | −70.2 | −58.0 | −35.0 | −24.4 | −16.7 | −13.0 | 0.478 |
| REINFORCE, α = 2^-14 | −74.1 | −69.5 | −51.2 | −39.0 | −25.5 | −16.8 | 0.355 |
| with baseline, α_θ = 2^-9, α_w = 2^-6 | −56.4 | −23.1 | −13.1 | −11.9 | −11.7 | −11.8 | 0.603 |
| actor-critic, α_θ = 2^-6, α_w = 2^-4 | −44.5 | −12.7 | −11.9 | −12.2 | −11.9 | −12.1 | 0.596 |

As in Figure 13.1, REINFORCE converges toward v* = −11.66 at a speed set by α: 2^-12 reaches it within 1000
episodes and 2^-14 is still far off. As in Figure 13.2, the baseline lets a much larger α_θ be used and reaches
v* in about 100 episodes. The actor-critic learns fastest here, near v* by episode 50, and then stays between −11.9 and −12.2
with these fixed step sizes.

Reference implementation (Python, for cross-checking numbers only): `chapter13/short_corridor.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 13`
