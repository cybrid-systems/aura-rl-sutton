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
| 7 | n-step bootstrapping | ✅ Fig 7.2 n-step TD (19-state random walk); n-step Sarsa, n-step Expected Sarsa, n-step Tree Backup on cliff walking; off-policy IS n-step Sarsa and Q(σ) TODO |
| 8 | Planning (Dyna) | stub |
| 9 | On-policy prediction with approximation | stub |
| 10 | On-policy control with approximation | stub |
| 11 | Off-policy with approximation | stub |
| 12 | Eligibility traces | stub |

Each `chapters/chNN_*/README.md` lists the algorithms and figures planned for that chapter. [STATE.txt](STATE.txt) has the same status in key=value form.

每章 `chapters/chNN_*/README.md` 列出该章要重写的算法和对应图表；[STATE.txt](STATE.txt) 是机器可读的进度。

## Aura version / 锁定的 Aura 版本

Tested against Aura `main` at **`2b36f9f7e27135be16f87327c2d1c77eda722fec`** (2026-10-11). Chapters 2–4 were first written against `549fdd3`, Chapters 5–6 against `2f815c188`; all pass at the new pin.

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
scripts/run_chapter.sh 7                # n-step TD / Sarsa / Expected Sarsa / Tree Backup (about 20 min)
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

Seed 2026, Soft face, aarch64 dev container. Chapter 5 and Ex 6.2/6.5–6.7 were measured at Aura `2f815c188`; Fig 6.2, Fig 6.3 and Chapter 7 at `2b36f9f7e`. Run sizes are smaller than the book's
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

Tests (`scripts/run_tests.sh`): 82 checks in 7 files, all pass at `2b36f9f7e` (Ch6 part 2: 7 checks in 93 s; Ch7: 12 checks in 102 s).

## Layout / 目录

```text
lib/rl/       rng (Park–Miller LCG, Box–Muller), vec helpers, tuple (cons-built lists), check (test oracle)
lib/rl/       (also) knobs: RL_* run-size knobs from the environment
lib/envs/     gridworld, blackjack, cliffwalking, random-walk, windy
lib/algos/    bandit (Ch2), dp (Ch3–4), mc (Ch5: MC prediction, MC ES, ε-soft, off-policy IS),
              td (Ch6: TD(0), Sarsa, Q-learning, Expected Sarsa, Double Q-learning),
              td-batch (Fig 6.2 batch TD / MC), nstep (Ch7: n-step TD, Sarsa, Expected Sarsa, Tree Backup)
lib/oracle/   exact blackjack v_π and π_* tables (generated by tests/oracle/blackjack_exact.py)
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
- Run sizes are modest because file mode never frees closures; long runs grow by a few KB per episode. Per-step helpers recurse through top-level procedures instead of named `let`, which allocates a closure per entry.
- `scripts/run_tests.sh` also fails a test file that prints no `PASS` line or a `load_module_file:` / `<error>` line: a failed `require` skips the rest of the file and exits 0.

Details and upstream issue links are in [IMPROVEMENTS.md](IMPROVEMENTS.md).

## Reference and license / 参考与许可

Algorithms are reimplemented from the book's pseudocode. [ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction) (MIT) is used only to cross-check numbers. No code or text is copied from it or from the book.

算法依据书中伪代码独立实现；ShangtongZhang 的 Python 仓库只用于核对数值，未复制其代码或书中文字。

Licensed under the [Apache License 2.0](LICENSE).
