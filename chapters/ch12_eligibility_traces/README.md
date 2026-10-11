# Chapter 12 — Eligibility Traces

Status: done (19-state walk Fig 12.3 / 12.6 / 12.8; mountain car Fig 12.10 / 12.11 at small sizes)

| Driver | Book | What it does |
|---|---|---|
| `random_walk_lambda.aura` | Fig 12.3, 12.6, 12.8 | offline λ-return, TD(λ) with accumulating traces and true online TD(λ) with dutch traces on the 19-state walk; RMS error averaged over the first 10 episodes for λ ∈ {0, .4, .8, .9, .95, .975, .99, 1} × α ∈ {.1, .2, .4, .6, .8, 1}; 3 runs by default (book 100), about 3 min |
| `mountain_car_lambda.aura` | Fig 12.10, 12.11 | Sarsa(λ) with replacing traces for λ ∈ {0, .68, .84, .92, .96} at α = 0.5/8; at λ = 0.9: replacing vs accumulating traces vs true online Sarsa(λ) for α = 0.2, 0.5, 0.9 (/8); mean steps over the first 10 episodes, 1 run (book: 50 episodes, 100 runs) |

Library code: `lib/algos/traces.aura` (19-state walk, the three prediction methods), `lib/algos/sarsa-lambda.aura`
(Sarsa(λ) and true online Sarsa(λ) on the Chapter 10 tile coder). Tests: `tests/test_ch12_traces.aura`.

Notes:

- The walk is tabular, written as linear with one-hot features: z and w are 21-slot vectors.
- Offline λ-return: weights are frozen during the episode. At the end, G^λ_t is built backwards with the
  episode-start weights, G^λ_t = (1 − λ) v(S_{t+1}) + λ G^λ_{t+1}, G^λ_{T−1} = R, and the updates are applied in time
  order.
- Each run draws its 10 episodes once and every (method, λ, α) replays them (common random numbers), so the three
  tables are directly comparable. A diverging configuration counts as an error of 1.0 per episode.
- `tests/oracle/lambda_walk.py` reimplements the three methods and the Park–Miller PRNG in Python. With the same
  seed it gives the same errors to 7 digits, and the test checks that.
- Mountain car traces are sparse. Only weights with |z| ≥ 0.01 stay in an active list (about 44 steps of history
  at λ = 0.9). Touching all 2 904 weights per step would be far too slow on the Soft interpreter. Even so, a
  Sarsa(λ) step costs 4–6 ms against 1 ms for one-step Sarsa, so the defaults are small.

Result at the defaults (3 runs; best error over α for each λ):

| λ | offline λ-return | TD(λ) | true online TD(λ) |
|---|---|---|---|
| 0 | 0.362 | 0.340 | 0.340 |
| 0.4 | 0.288 | 0.272 | 0.270 |
| 0.8 | 0.255 | 0.258 | 0.246 |
| 0.9 | 0.279 | 0.276 | 0.275 |
| 0.95 | 0.309 | 0.331 | 0.301 |
| 0.99 | 0.401 | 0.521 | 0.399 |
| 1 | 0.510 | 0.795 | 0.510 |

As in the book, true online TD(λ) tracks the offline λ-return, while TD(λ) with accumulating traces breaks down
at large α for λ ≥ 0.9 (errors near 1.0 in the TD(λ) table).

Mountain car at the defaults (1 run, mean steps over the first 10 episodes, about 8 min):

| Sarsa(λ), replacing, α = 0.5/8 | λ = 0: 600 | 0.68: 520 | 0.84: 557 | 0.92: 549 | 0.96: 493 |
|---|---|---|---|---|---|

| α (/8), λ = 0.9 | replacing | accumulating | true online |
|---|---|---|---|
| 0.2 | 766 | 593 | 594 |
| 0.5 | 500 | 541 | 415 |
| 0.9 | 485 | 2 496 | 381 |

Accumulating traces fall apart at α = 0.9/8 and true online Sarsa(λ) is best at every α, as in Figure 12.11. One
run of 10 episodes is too short to separate the λ values of Figure 12.10.

Reference implementation (Python, for cross-checking numbers only): `chapter12/random_walk.py, mountain_car.py, lambda_effect.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 12`
