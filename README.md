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
| 5 | Monte Carlo | stub (blackjack env ready) |
| 6 | TD learning | stub (random-walk and cliff-walking envs ready) |
| 7 | n-step bootstrapping | stub |
| 8 | Planning (Dyna) | stub |
| 9 | On-policy prediction with approximation | stub |
| 10 | On-policy control with approximation | stub |
| 11 | Off-policy with approximation | stub |
| 12 | Eligibility traces | stub |

Each `chapters/chNN_*/README.md` lists the algorithms and figures planned for that chapter. [STATE.txt](STATE.txt) has the same status in key=value form.

每章 `chapters/chNN_*/README.md` 列出该章要重写的算法和对应图表；[STATE.txt](STATE.txt) 是机器可读的进度。

## Aura version / 锁定的 Aura 版本

Tested against Aura `main` at **`549fdd3497f666be4df89b234f7ec31e6d6fa7cf`** (2026-10-11).

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

## Layout / 目录

```text
lib/rl/       rng (Park–Miller LCG, Box–Muller), vec helpers, tuple (cons-built lists), check (test oracle)
lib/envs/     gridworld, blackjack, cliffwalking, random-walk
lib/algos/    bandit (Ch2), dp (Ch3–4: policy evaluation / iteration, value iteration)
chapters/     one directory per chapter: experiment drivers (*.aura) + README.md
tests/        oracle tests; scripts/run_tests.sh fails on any FAIL line or crash
scripts/      env.sh, run_chapter.sh, run_tests.sh
```

## Aura workarounds in this code / 代码中的 Aura 规避写法

- Small lists in hot paths are built with `cons` (`lib/rl/tuple.aura`), not `list`: each `list` call costs memory proportional to the whole pair heap.
- Loops use `(if c (begin … (loop …)) #f)` rather than `when` / `unless` / `and` / `or`: a tail call in those forms is not eliminated and overflows the C stack after about 700 iterations.
- Symbol tags are compared with `equal?`, not `eq?`: a string literal with the same text re-points `(quote sym)`.

Details and upstream issue links are in [IMPROVEMENTS.md](IMPROVEMENTS.md).

## Reference and license / 参考与许可

Algorithms are reimplemented from the book's pseudocode. [ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction) (MIT) is used only to cross-check numbers. No code or text is copied from it or from the book.

算法依据书中伪代码独立实现；ShangtongZhang 的 Python 仓库只用于核对数值，未复制其代码或书中文字。

Licensed under the [Apache License 2.0](LICENSE).
