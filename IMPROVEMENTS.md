# Aura findings from the RL port / 移植中发现的 Aura 问题

Aura tip: `549fdd3497f666be4df89b234f7ec31e6d6fa7cf`. Each bug has a minimal repro and an upstream issue.
Soft = `AURA_SANDBOX=off AURA_PIPELINE_STRICT=0`; default = no env vars (Restricted + strict pipeline).

## Bugs filed upstream / 已提 issue

| # | Finding | Hit in | Workaround here | Issue |
|---|---|---|---|---|
| 1 | `list` costs O(N²) memory and time over a run: `pairs.reserve(pairs.size() + n)` on a `pmr::vector` backed by a monotonic arena, so every call reallocates and never frees. 10 000 `(list 1 i)` calls peak at 1.58 GB RSS; the same loop with `cons` peaks at 100 MB. `append` / `reverse` / `map` / `filter` / `list-sort` / JSON use the same reserve pattern. | Ch3 value iteration hit 4 GB and was killed | `lib/rl/tuple.aura` (cons-built `tup2`/`tup3`/`tup4`, `dp-det`) | [#4453](https://github.com/cybrid-systems/aura/issues/4453) |
| 2 | A self tail call inside `when` / `unless` / `and` / `or` is not eliminated, so a loop of more than ~700 iterations ends in SIGSEGV. Plain non-tail recursion of depth 700–1000 also ends in SIGSEGV: the `MAX_C_STACK_DEPTH = 700` guard in `eval_flat` never returns its "recursion depth exceeded" error. | Ch2 runs with more than ~700 steps | loops written as `(if c (begin … (lp …)) #f)` | [#4454](https://github.com/cybrid-systems/aura/issues/4454) |
| 3 | `(eq? s 'ucb)` turns `#f` once a string literal `"ucb"` has been read after `s` was bound: quoted symbols are string-heap values (`(symbol? 'a)` → `#f`, `(string? 'a)` → `#t`), and the later literal re-points `(quote ucb)`. This is a residual of closed #2568. | UCB silently fell through to the gradient branch (10% optimal) when its label was `"ucb"` | `equal?` for symbol tags | [#4455](https://github.com/cybrid-systems/aura/issues/4455) |
| 4 | `vector-ref` with a float index (`(vector-ref v 1.0)`) aborts the process with SIGABRT. `vector-set!` checks `is_int` and returns an error; `vector-ref` does not check. | index arithmetic with `floor` / `round` results | `inexact->exact` before indexing | [#4456](https://github.com/cybrid-systems/aura/issues/4456) |
| 5 | Default face: when a file defines a procedure, every top-level form runs twice (`(define (f x) …) (display "one")` prints `one` twice). There is no error, unlike the trigger in closed #4355. | every chapter driver on the default face | run on Soft | [#4457](https://github.com/cybrid-systems/aura/issues/4457) |
| 6 | std lib: `std/random` `shuffle` returns a nested garbage list (`(cons (car shuffled) (car shuffled))` drops `picked`). `std/math` `expt` with a non-integer or negative exponent recurses forever and ends in SIGSEGV (`(expt 2 0.5)`). | RNG / softmax helpers | own `rl/rng`, `exp`/`pow` | [#4458](https://github.com/cybrid-systems/aura/issues/4458) |

## Improvement notes (not filed) / 改进点（未提 issue）

- Default face refuses named `let`, `while`, `do`, `random`, `exact->inexact` with "tree-walker fallback forbidden in production pipeline (#2213)". The same message is shown for a plain unbound variable, which makes typos hard to see.
- Restricted (default sandbox) denies `vector-set!` without a Mutate grant, but the denial is silent: `(display (vector-set! v 1 7))` prints `<unknown>`, the vector is unchanged, and the run exits 0. Numeric code computes wrong answers with no warning.
- Errors from primitives display as `<unknown>` and do not stop the program or change the exit code. There is no `exit` primitive, so test runners must grep for `FAIL`.
- `(display (vector 1 2 3))` prints `<vector[0]>`, which shows the heap slot and not the contents or length. `vector->list` is needed to inspect values.
- Missing common Scheme procedures: `do`, `exact->inexact`, `exact`, `vector-fill!`, `vector-map`, `vector-copy`, `assoc`, `iota`, `exit`.
- `(/ 7 2)` → `3` (integer division) while `(/ 7.0 2)` → `3.5`. Averages need an explicit `(* 1.0 x)`.
- Floats print with 6 significant digits (`123456.789` → `123457`, `3.0` → `3`).
- Soft interpreter speed: about 40 µs per simple loop iteration and about 2 ms per bandit step (10 arms). That is why Ch2 defaults to 20 runs × 300 steps.
- File mode echoes the value of the last top-level form (a trailing `#t` / `#f` after program output).
- `AURA_SANDBOX=strict` fails while loading the std prelude ("Soft oneshot std prelude failed … tree-walker fallback forbidden").
