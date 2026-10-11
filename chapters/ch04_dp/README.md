# Chapter 4 — Dynamic Programming

Status: done.

| Driver | Book | What it does |
|---|---|---|
| `grid_world.aura` | Example 4.1, Figure 4.1 | iterative policy evaluation (in-place vs synchronous), policy iteration, value iteration on the 4×4 gridworld |
| `car_rental.aura` | Example 4.2, Figure 4.2 | Jack's car rental by policy iteration: prints π1 … π4 and v_π4 |
| `gambler.aura` | Example 4.3, Figure 4.3 | the gambler's problem (p_h = 0.4) by value iteration: value estimates after sweeps 1, 2, 3 and at convergence, final policy |

**Car rental** (`lib/envs/car-rental.aura`). The full model of the book: Poisson requests
(λ = 3, 4) and returns (λ = 3, 2), tails cut at 25, at most 20 cars per location, at most 5 moved
($2 each), $10 per rental, γ = 0.9. After the overnight move the two locations evolve
independently, so the expected next value factorizes:
E[n1, n2] = R1[n1] + R2[n2] + γ Σ T1[n1][n1'] Σ T2[n2][n2'] V[n1'][n2'], and q(s, a) = E[after move] − 2|a|.
A synchronous evaluation sweep fills W = V T2ᵀ and then E (two 21³ passes), instead of summing
26² request × return pairs per state. Policy iteration from "move nothing" with evaluation to
θ = 1e-4 changes 318 / 272 / 79 / 8 / 0 states (126 / 91 / 80 / 45 / 14 sweeps) and stops at π4,
the book's optimal policy. v_π4 runs from 421.4 at (0, 0) to 637.0 at (20, 20). Every number
matches `tests/oracle/car_rental.py` (numpy, same model) exactly. 115 s on a RelWithDebInfo build.

**Gambler's problem** (`lib/envs/gambler.aura`). v(0) = 0 and v(100) = 1 are fixed; in-place
value iteration to θ = 1e-9 takes 17 sweeps. v(25) = 0.16, v(50) = 0.4, v(75) = 0.64,
v(99) = 0.9643. The printed policy takes the smallest stake within 1e-6 of the best (many
stakes tie): 1, 2, …, 12, 12, 11, …, 1, 25 on each quarter, with 50 at s = 50, which is the
shape of Figure 4.3. Matches `tests/oracle/gambler.py`. 1 s.

Checks (`tests/test_ch03_ch04_dp.aura`, `tests/test_ch04_dp_examples.aura`): published
gridworld values; Poisson and transition rows sum to 1; expected rent 0 / 30 / 40; move
feasibility; v after 10 sweeps of π0 at three states and the first improvement (321 states
changed, four actions) against the oracle; gambler values, sweep count, sweep-1 value and
policy against the oracle.

Knobs: `RL_THETA` (car rental), `RL_PH` (gambler).

Reference implementation (Python, for cross-checking numbers only): `chapter04/grid_world.py, car_rental.py, car_rental_synchronous.py, gamblers_problem.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 4`
