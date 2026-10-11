# aura-rl-sutton

Aura implementations of the algorithms in Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.).
The project also works as a stress test for [Aura](https://github.com/cybrid-systems/aura): Aura bugs and gaps found while porting are reported upstream and tracked in [IMPROVEMENTS.md](IMPROVEMENTS.md).

用 [Aura](https://github.com/cybrid-systems/aura) 重写 Sutton & Barto《强化学习导论》（第 2 版）中的算法。移植过程中发现的 Aura bug 和改进点会提到 Aura 仓库，并记录在 [IMPROVEMENTS.md](IMPROVEMENTS.md)。

## Status / 进度

| Chapter | Topic | Status |
|---|---|---|
| 2 | Multi-armed bandits | ✅ Fig 2.2–2.5 (ε-greedy, optimistic init, UCB, gradient bandit); Fig 2.6 TODO |
| 3 | Finite MDPs | ✅ Fig 3.2 (v_π), Fig 3.5 (v_*, π_*) |
| 4 | Dynamic programming | ✅ 4×4 gridworld: policy evaluation, policy iteration, value iteration; car rental / gambler TODO |
| 5 | Monte Carlo | ✅ Fig 5.1–5.4, Sec 5.4: first-/every-visit MC prediction, Monte Carlo ES, ε-soft on-policy control, ordinary vs weighted importance sampling |
| 6 | TD learning | ✅ Ex 6.2 (TD(0) vs constant-α MC), Fig 6.2 batch updating, 6.5 windy gridworld (Sarsa), 6.6 cliff walking (Sarsa / Q-learning / Expected Sarsa), Fig 6.3 interim / asymptotic α sweep, 6.7 maximization bias (Double Q-learning) |
| 7 | n-step bootstrapping | ✅ Fig 7.2 n-step TD (19-state random walk); n-step Sarsa, n-step Expected Sarsa, n-step Tree Backup, off-policy IS n-step Sarsa and off-policy n-step Q(σ) on cliff walking |
| 8 | Planning (Dyna) | ✅ Fig 8.2 Dyna-Q (Dyna maze), Fig 8.4 / 8.5 Dyna-Q vs Dyna-Q+ (blocking / shortcut maze); prioritized sweeping, Fig 8.7 / 8.8 TODO |
| 9 | On-policy prediction with approximation | ✅ 1000-state random walk: Fig 9.1 gradient MC and Fig 9.2 semi-gradient TD(0) / n-step TD with state aggregation, Fig 9.8 coarse coding, Fig 9.10 tile coding vs aggregation; Fig 9.5 polynomial / Fourier TODO |
| 10 | On-policy control with approximation | ✅ mountain car with tile coding: Fig 10.1 cost-to-go, Fig 10.2 semi-gradient Sarsa α sweep, Fig 10.3 n-step Sarsa; Fig 10.4 and access control (Fig 10.5) TODO |
| 11 | Off-policy with approximation | stub |
| 12 | Eligibility traces | stub |

Each `chapters/chNN_*/README.md` lists the algorithms and figures planned for that chapter. [STATE.txt](STATE.txt) has the same status in key=value form.

每章 `chapters/chNN_*/README.md` 列出该章要重写的算法和对应图表；[STATE.txt](STATE.txt) 是机器可读的进度。

## Aura version / 锁定的 Aura 版本

Tested against Aura `main` at **`5cc915687`** (2026-10-12), built with `-DCMAKE_BUILD_TYPE=RelWithDebInfo`. Chapters 2–4 were first written against `549fdd3`, Chapters 5–6 against `2f815c188`, Chapter 7 (first part) against `2b36f9f7e`, the rest of Chapter 7 and Chapter 8 against `f093a8887`; all pass at the new pin.

Build Aura with an explicit build type. Aura's CMake does not set a default, so a plain `cmake -B build` gives an unoptimized binary that runs these drivers 3–5× slower.

Aura 要用 `-DCMAKE_BUILD_TYPE=RelWithDebInfo` 构建；不指定构建类型时是未优化的二进制，速度慢 3–5 倍。

All code runs on the **Soft** face:

```bash
export AURA_SANDBOX=off          # Restricted denies vector-set! without a Mutate grant
export AURA_PIPELINE_STRICT=0    # the strict pipeline refuses named let / while (tree-walker fallback)
```

`scripts/env.sh` sets both, plus `AURA_PATH`. Point it at your Aura build with `AURA_BIN`:

所有代码在 Soft 模式下运行（见上面两个环境变量，`scripts/env.sh` 会自动设置）。用 `AURA_BIN` 指定 Aura 可执行文件：

```bash
export AURA_BIN=$HOME/aura/build/aura   # required; AURA_LIB defaults to $(dirname $AURA_BIN)/../lib
scripts/run_chapter.sh 2                # 10-armed testbed (RL_RUNS / RL_STEPS / RL_SEED to tune)
scripts/run_chapter.sh 3                # 5×5 gridworld
scripts/run_chapter.sh 4                # 4×4 gridworld DP
scripts/run_chapter.sh 5                # blackjack MC (about 7 min at the defaults)
scripts/run_chapter.sh 6                # TD: random walk, batch, windy, cliff, α sweep, max bias (about 35 min)
scripts/run_chapter.sh 7                # n-step TD / Sarsa / Expected Sarsa / Tree Backup / off-policy IS / Q(σ) (about 40 min)
scripts/run_chapter.sh 8                # Dyna-Q maze, Dyna-Q vs Dyna-Q+ on blocking / shortcut mazes (about 10 min)
scripts/run_chapter.sh 9                # 1000-state walk: aggregation, n-step TD, coarse / tile coding (about 10 min, release build)
scripts/run_chapter.sh 10               # mountain car: semi-gradient Sarsa, n-step Sarsa (about 3 min, release build)
scripts/run_tests.sh                    # oracle checks against published values
```

Expected Chapter 3 output (Fig 3.2 / 3.5), about 5 s on an aarch64 dev container:

```text
Figure 3.2 — v_pi (random policy), sweeps=47
    3.3    8.8    4.4    5.3    1.5
    1.5      3    2.3    1.9    0.5
    0.1    0.7    0.7    0.4   -0.4
     -1   -0.4   -0.4   -0.6   -1.2
   -1.9   -1.3   -1.2   -1.4     -2
Figure 3.5 — v_* (value iteration), sweeps=24
     22   24.4     22   19.4   17.5
   19.8     22   19.8   17.8     16
   17.8   19.8   17.8     16   14.4
     16   17.8     16   14.4     13
   14.4     16   14.4     13   11.7
```

Chapter 2 defaults to 20 runs × 300 steps (the book uses 2000 × 1000) because the Soft interpreter takes about 2 ms per bandit step (the full chapter run takes about 5 min). Raise `RL_RUNS` / `RL_STEPS` for smoother numbers.

第 2 章默认 20 次 × 300 步（书中是 2000 × 1000），因为 Soft 解释器每步约 2 ms；可用 `RL_RUNS` / `RL_STEPS` 调大。

## Results at the defaults / 默认参数下的结果

Seed 2026, Soft face, aarch64 dev container. Chapter 5 and Ex 6.2/6.5–6.7 were measured at Aura `2f815c188`; Fig 6.2, Fig 6.3 and on-policy Chapter 7 at `2b36f9f7e`; off-policy Chapter 7 and Chapter 8 at `f093a8887`; Chapters 9–10 at `5cc915687`. Wall times for Chapters 2–8 come from an unoptimized Aura build (no `CMAKE_BUILD_TYPE`); Chapters 9–10 use a RelWithDebInfo build, which is 3–5× faster. Run sizes are smaller than the book's
because the Soft interpreter takes about 1.5 ms per blackjack episode and file mode never frees closures
(memory grows with the run, [#4459](https://github.com/cybrid-systems/aura/issues/4459)). Every driver has
`RL_*` knobs to raise them.

种子 2026，Soft 模式。运行规模比书中小（解释器速度 + 文件模式不回收闭包，见 #4459），可用 `RL_*` 环境变量调大。

**Chapter 5 (blackjack; exact values from `lib/oracle`, a DP over the same rules)**

| Driver | Result | Book / exact | Wall |
|---|---|---|---|
| Fig 5.1, 10 000 episodes | RMS vs exact v_π: 0.076 (no usable ace), 0.276 (usable ace); first-visit == every-visit | v(13, usable, 2) = −0.27726 | 48 s |
| Fig 5.2, MC ES, 50 000 episodes | greedy policy agrees with exact π_* on 92/100 (no ace) and 98/100 (usable ace) states; mean return −0.046 | optimal −0.047, stick-20 −0.354 | 284 s (with ε-soft) |
| Sec 5.4, ε-soft (ε = 0.1), 50 000 episodes | 91/100 and 86/100 states; mean return −0.037 | — | |
| Fig 5.3, 20 runs | MSE at 1 / 10 / 100 / 1 000 episodes: ordinary IS 6.03 / 1.80 / 0.162 / 0.0119, weighted IS 0.244 / 0.778 / 0.129 / 0.0096 | weighted IS lower early | 68 s |
| Fig 5.4 | ordinary IS estimates of v = 1 stay heavy-tailed after 10 000 episodes (0.52–0.94 over 5 runs) | infinite variance | |

**Chapter 6**

| Driver | Result | Book | Wall |
|---|---|---|---|
| Ex 6.2 random walk, 100 runs | RMS after 100 episodes: TD(0) α = 0.05 → 0.037, α = 0.1 → 0.052; MC α = 0.02 → 0.089, α = 0.04 → 0.112 | TD beats MC | 242 s |
| Fig 6.2 batch updating, 20 runs × 100 episodes, α = 0.001 | RMS at episodes 10 / 50 / 100: batch TD 0.100 / 0.061 / 0.040, batch MC 0.173 / 0.093 / 0.057 (23 sweeps per episode on average) | batch TD below batch MC | 203 s |
| Ex 6.5 windy gridworld, Sarsa | 170 episodes in 7 852 steps; greedy path 15 steps | ~8 000 steps; optimal 15 | 10 s |
| Ex 6.6 cliff walking, 10 runs × 500 | mean reward per episode, episodes 451–500: Sarsa −23.2, Q-learning −51.8, Expected Sarsa −20.5; greedy paths 17 / 13 (cliff edge) / 15 | Sarsa ≈ −25, Q ≈ −50 | 628 s |
| Fig 6.3 α sweep, interim 4 runs × 100 episodes, asymptotic 1 run × 500 | interim reward at α = 0.1 / 0.5 / 1.0: Sarsa −138.8 / −70.0 / −75.8, Expected Sarsa −135.4 / −59.0 / −45.5, Q-learning −154.1 / −81.1 / −73.7; asymptotic at α = 1.0: −57.1 / −27.1 / −54.4 | Expected Sarsa best and flat up to α = 1; Sarsa degrades at large α | 762 s |
| Ex 6.7 maximization bias, 200 runs | % `left` from A, episodes 11–60: Q-learning 85.6, Double Q 24.3; episodes 261–300: 12.9 vs 6.9 | optimal 5 % | 261 s |

**Chapter 7**

| Driver | Result | Book | Wall |
|---|---|---|---|
| Fig 7.2 n-step TD, 19-state walk, 10 runs × 10 episodes | best RMS per n: n = 1 0.345 (α = 0.8), n = 2 0.257 (0.6), n = 4 0.262 (0.4), n = 8 0.254 (0.2), n = 16 0.302 (0.1); large α hurts large n | intermediate n best, minimum ≈ 0.25–0.3 | 343 s |
| n-step control, cliff walking, 3 runs × 200 episodes, α = 0.2 | online reward (episodes 101–200) for n = 1 / 2 / 4 / 8: Sarsa −28.0 / −25.2 / −24.0 / −26.7, Expected Sarsa −28.1 / −22.0 / −20.9 / −33.6, Tree Backup −44.5 / −47.2 / −23.6 / −47.1; Tree Backup greedy path 13 (cliff edge) for n = 1, 2 | on-policy safer online; Tree Backup learns q* | 860 s |
| off-policy n-step control, cliff walking, ε_b = 0.1, greedy target, 3 runs × 200 episodes, α = 0.2 | online reward (episodes 101–200) / greedy-target return: IS n-step Sarsa n = 1 −48.6 / −13, n = 2 −27.7 / −15, n = 4 −26.3 / −17, n = 8 −33.6 / −19; Q(σ), n = 4: σ = 0 −29.7 / −15, σ = 0.5 −25.2 / −17, σ = 1 −26.7 / −17, σ random −30.8 / −17 | n = 1 learns the cliff-edge q* path; with a greedy target ρ is 0 after any exploratory action, so larger n learns the greedy path more slowly in 200 episodes | 1122 s (under load) |

**Chapter 8**

| Driver | Result | Book | Wall |
|---|---|---|---|
| Fig 8.2 Dyna maze, 2 runs × 50 episodes | steps per episode at episodes 1 / 2 / 3 / 5 / 10 / 50: n = 0 868 / 616 / 545 / 73 / 71 / 21, n = 5 868 / 135 / 41 / 21 / 18 / 16, n = 50 868 / 40 / 20 / 14 / 15 / 17; mean over episodes 11–50: 42.4 / 15.7 / 15.8 | first episode the same for all n; n = 50 near optimal (14) by episode 3, n = 0 needs about 25 episodes | 147 s |
| Fig 8.4 blocking maze, 3 runs × 3000 steps | cumulative reward at steps 1000 / 1500 / 3000: Dyna-Q 51 / 56.7 / 110, Dyna-Q+ 55.3 / 57.3 / 135.3; flat after the change at step 1000, Dyna-Q+ recovers faster | Dyna-Q+ ahead after the change | 440 s (both mazes) |
| Fig 8.5 shortcut maze, 3 runs × 6000 steps | reward gained in steps 3001–6000: Dyna-Q 164 (about one goal per 18 steps, long path), Dyna-Q+ 225.7 (about one per 13 steps, shortcut) | Dyna-Q+ finds the shortcut, Dyna-Q does not | |

**Chapter 9 (1000-state random walk; exact v_π from `lib/oracle/walk1000-exact.aura`)**

| Driver | Result | Book | Wall |
|---|---|---|---|
| Fig 9.1 / 9.2 left, 10 groups, 2 000 episodes, α = 0.001 (MC) / 0.01 (TD) | gradient MC tracks the μ-weighted group mean of v_π (group 1: −0.825 vs −0.830; group 10: 0.802 vs 0.829), RMS 0.082; semi-gradient TD(0) is pulled toward 0 at the ends (−0.723 / 0.754), RMS 0.125; μ is 2.8–3.1 % in the end groups and 16–18 % in the middle | book: 100 000 episodes at α = 2e-5 / 2e-4; TD has the larger asymptotic error | 60 s |
| Fig 9.2 right, 20 groups, 10 runs × 10 episodes | RMS over the first 10 episodes: best 0.274 (n = 4, α = 0.4); n = 1 best 0.341 (α = 0.8), n = 8 0.280 (α = 0.2), n = 64 0.470 (α = 0.1) | intermediate n best, minimum ≈ 0.25–0.3 | 69 s |
| Fig 9.8 coarse coding, square wave | MAE after 10 / 160 / 10 240 samples: width 0.2 → 0.416 / 0.094 / 0.075, 0.4 → 0.321 / 0.119 / 0.104, 1.0 → 0.368 / 0.105 / 0.034; after 10 samples the broad features are non-zero across most of [0, 2), the narrow ones only near the samples | width shapes early generalisation; all widths approach the square wave | 54 s |
| Fig 9.10, tiles 200 wide, α = 2e-4, 5 000 episodes, 1 run | RMS at episodes 1 000 / 2 500 / 5 000: one tiling 0.164 / 0.122 / 0.131, 10 tilings (offset 20) 0.215 / 0.128 / 0.095; best possible (μ-weighted fit): 0.112 vs 0.011 | book (50 tilings, offset 4, 30 runs): tile coding lower throughout; here it starts slower and ends lower | 394 s |

**Chapter 10 (mountain car, 8 tilings, ε = 0)**

| Driver | Result | Book | Wall |
|---|---|---|---|
| Fig 10.1, α = 0.3/8 | first episode 2 875 steps; cost-to-go after 100 episodes peaks at about 80 near (−0.56, 0) and falls toward the goal and along the spiral of high-energy states | same shape | 139 s (with Fig 10.2) |
| Fig 10.2, 1 run × 100 episodes | steps at episodes 1 / 10 / 50, mean of episodes 91–100: α = 0.1/8 3 531 / 670 / 364, 232; α = 0.2/8 1 884 / 495 / 251, 163; α = 0.5/8 2 379 / 239 / 163, 142 | α = 0.5/8 learns fastest; ≈ 150–200 steps after 100 episodes | |
| Fig 10.3, 1 run × 100 episodes | mean steps, episodes 1–50 / 51–100: n = 1 (α = 0.5/8) 281 / 154, n = 8 (α = 0.3/8) 250 / 128 | n = 8 better | 49 s |

Tests (`scripts/run_tests.sh`): 148 checks in 11 files, all pass at `5cc915687` in 3 min 11 s with a RelWithDebInfo build (Ch9: 24 checks in 34 s; Ch10: 17 checks in 14 s).

## Layout / 目录

```text
lib/rl/       rng (Park–Miller LCG, Box–Muller), vec helpers, tuple (cons-built lists), check (test oracle)
lib/rl/       (also) knobs: RL_* run-size knobs from the environment
lib/envs/     gridworld, blackjack, cliffwalking, random-walk, windy, maze (Dyna / blocking / shortcut),
              walk1000 (Example 9.1), mountain-car (Example 10.1)
lib/algos/    bandit (Ch2), dp (Ch3–4), mc (Ch5: MC prediction, MC ES, ε-soft, off-policy IS),
              td (Ch6: TD(0), Sarsa, Q-learning, Expected Sarsa, Double Q-learning),
              td-batch (Fig 6.2 batch TD / MC), nstep (Ch7: n-step TD, Sarsa, Expected Sarsa, Tree Backup,
              off-policy IS n-step Sarsa, Q(σ)), dyna (Ch8: Dyna-Q, Dyna-Q+),
              approx (Ch9: tile coder, gradient MC, semi-gradient n-step TD, coarse coding),
              semigrad-sarsa (Ch10: mountain-car tile coder, semi-gradient n-step Sarsa)
lib/oracle/   exact blackjack v_π and π_* tables (tests/oracle/blackjack_exact.py), exact v_π of the
              1000-state walk (tests/oracle/walk1000_exact.py)
chapters/     one directory per chapter: experiment drivers (*.aura) + README.md
tests/        oracle tests; scripts/run_tests.sh fails on any FAIL line or crash
scripts/      env.sh, run_chapter.sh, run_tests.sh
```

## Aura workarounds in this code / 代码中的 Aura 规避写法

- Small lists in hot paths are built with `cons` (`lib/rl/tuple.aura`), not `list`: each `list` call costs memory proportional to the whole pair heap.
- Loops use `(if c (begin … (loop …)) #f)` rather than `when` / `unless` / `and` / `or`: a tail call in those forms is not eliminated and overflows the C stack after about 700 iterations.
- Symbol tags are compared with `equal?`, not `eq?`: a string literal with the same text re-points `(quote sym)`.
- Lists are reversed with `tup-reverse` (cons-built), not `reverse`, which has the same reserve pattern as `list`.
- Every division whose denominator can be zero is guarded: `/` by a non-literal zero silently returns `0`.
- Numbers never come from strings or booleans inside arithmetic: `(* 1.0 "0.95")` is `0` and `(+ 1 #f)` is `1`, so knobs go through `string->number` and numeric tables start at `0.0`, never `#f`.
- Integer arithmetic stays far below 2^62 (the Park–Miller LCG keeps products below 2^46): results in [2^62, 2^63) abort the process.
- Run sizes are modest because file mode never frees closures; long runs grow by a few KB per episode. Per-step helpers recurse through top-level procedures instead of named `let`, which allocates a closure per entry.
- Test helpers never pass a value that may be a primitive error into a user procedure: an error passed to or returned from a user procedure at top level skips the rest of the file with exit status 0 ([#4465](https://github.com/cybrid-systems/aura/issues/4465)).
- Per-step state lives in module-level vectors (`walk1000`, `mountain-car`) and episodes use ring buffers, so a step allocates no list. Every call costs time proportional to the number of globals ([#4464](https://github.com/cybrid-systems/aura/issues/4464)), so hot helpers stay few and flat.
- `scripts/run_tests.sh` also fails a test file that prints no `PASS` line or a `load_module_file:` / `<error>` line: a failed `require` skips the rest of the file and exits 0.

Details and upstream issue links are in [IMPROVEMENTS.md](IMPROVEMENTS.md).

## Reference and license / 参考与许可

Algorithms are reimplemented from the book's pseudocode. [ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction) (MIT) is used only to cross-check numbers. No code or text is copied from it or from the book.

算法依据书中伪代码独立实现；ShangtongZhang 的 Python 仓库只用于核对数值，未复制其代码或书中文字。

Licensed under the [Apache License 2.0](LICENSE).
