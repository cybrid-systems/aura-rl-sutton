# Chapter 2 — Multi-armed Bandits

Status: done.

| Driver | Book | What it does |
|---|---|---|
| `ten_armed_testbed.aura` | Figures 2.2–2.5 | ε-greedy with sample averages, optimistic initial values, UCB, gradient bandit with / without baseline (true means offset by +4) |
| `parameter_study.aura` | Figure 2.6 | average reward over the first 1000 steps as a function of each method's parameter: ε-greedy ε ∈ 1/128 … 1/4, gradient bandit (with baseline) α ∈ 1/32 … 4, UCB c ∈ 1/16 … 4, greedy with optimistic Q1 ∈ 1/4 … 4 (α = 0.1) |

Code: `lib/algos/bandit.aura`. `bandit-param-point` seeds run r with `seed + r`, so every point
of the parameter study is measured on the same testbeds (common random numbers); the curves are
much smoother than independent runs of the same size. Powers of two are literals because `expt`
with a negative exponent never returns ([aura#4458](https://github.com/cybrid-systems/aura/issues/4458)).

Figure 2.6 at 50 runs × 1000 steps (seed 2026, `3034d4723` RelWithDebInfo, 13 min; the default
10 runs takes 2.5 min):

| Method | parameter: average reward | best |
|---|---|---|
| ε-greedy | 1/128: 1.089, 1/64: 1.182, 1/32: 1.254, 1/16: 1.303, 1/8: 1.264, 1/4: 1.096 | ε = 1/16 |
| gradient + baseline | 1/32: 1.066, 1/16: 1.264, 1/8: 1.356, 1/4: 1.363, 1/2: 1.319, 1: 1.255, 2: 1.029, 4: 0.853 | α = 1/4 |
| UCB | 1/16: 1.425, 1/8: 1.426, 1/4: 1.466, 1/2: 1.451, 1: 1.448, 2: 1.359, 4: 1.134 | c = 1/4 (flat 1/4–1) |
| optimistic greedy | 1/4: 1.237, 1/2: 1.327, 1: 1.424, 2: 1.391, 4: 1.301 | Q1 = 1 |

Every curve is an inverted U with its peak near the book's (ε ≈ 1/16, α ≈ 1/4, Q1 ≈ 1; UCB is
flat between c = 1/4 and 1), UCB is the best method and ε-greedy the worst, and the levels
(1.30 / 1.36 / 1.47 / 1.42 at the peaks) are close to the book's. After seeding, four draws are
discarded: Park–Miller states seeded with consecutive integers start with nearly equal uniforms,
and without the burn-in the 50 testbeds shared a high first arm, which put every curve about 0.3
above the book.

Checks (`tests/test_ch02_bandits.aura`): softmax; Figure 2.2 / 2.4 / 2.5 orderings; Figure 2.6
at 6 runs × 600 steps: ε = 1/16 beats 1/128 and 1/4, UCB c = 1 beats c = 4 and beats ε-greedy at
ε = 1/16, gradient α = 1/4 beats α = 1/32.

Knobs: `RL_RUNS`, `RL_STEPS`, `RL_SEED`.

Reference implementation (Python, for cross-checking numbers only): `chapter02/ten_armed_testbed.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 2`
