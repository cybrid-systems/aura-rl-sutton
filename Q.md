**Filed from:** cybrid-systems/aura-rl-sutton (Aura port of the Sutton & Barto RL algorithms)

## Summary

Basic number conversions do not follow R7RS, and some are missing:

- `round` rounds halves away from zero: `(round 0.5)` → `1`, `(round 2.5)` → `3`, `(round -2.5)` → `-3`. R7RS rounds to even: `0`, `2`, `-2`.
- `integer?` is `#f` for every float, including integral ones: `(integer? 2.0)`, `(integer? (round 2.4))` and `(integer? (floor 2.7))` are all `#f`. Since `floor` / `ceil` / `round` / `trunc` always return floats, `(integer? (round x))` is never true.
- `inexact->exact` exists, but its inverse `exact->inexact` does not, and neither do `exact`, `inexact`, `exact?`, `inexact?`, `truncate` or `ceiling` (only the non-standard `trunc` / `ceil`). Each is `unbound variable`; for `truncate` the hint is "did you mean 'trunc'?".

In the RL port, rounding helpers and tie-breaking code ported from Scheme or Python give different results at exact halves, and code that converts an index with `(round x)` and then checks `integer?` takes the wrong branch. `(* 1.0 n)` has to stand in for `exact->inexact`.

Aura `main` at `3034d4723` (RelWithDebInfo), file mode, Soft face (`AURA_SANDBOX=off AURA_PIPELINE_STRICT=0`). Same at `5cc915687`.

## Repro

```scheme
(display (round 0.5)) (newline)
(display (round 2.5)) (newline)
(display (round -2.5)) (newline)
(display (integer? 2)) (newline)
(display (integer? 2.0)) (newline)
(display (integer? (round 2.4))) (newline)
(display (integer? (floor 2.7))) (newline)
(display (inexact->exact 2.0)) (newline)
(display (exact->inexact 2)) (newline)
```

Output, exit 1:

```text
1
3
-3
#t
#f
#f
#f
2
error: 9:11: unbound variable: exact->inexact
   |
  9 | (display (exact->inexact 2)) (newline)
   |           ^^^^^^^^^^^^^^
```

Expected: `0`, `2`, `-2`, `#t`, `#t`, `#t`, `#t`, `2`, `2.0` (R7RS 6.2.6).

## Where

- `src/compiler/evaluator_primitives_math.cpp`, `round`: `make_float(std::round(to_double(a[0])))`. `std::round` rounds halves away from zero; `std::nearbyint` (default rounding mode) or `std::rint` rounds to even.
- `src/compiler/evaluator_primitives_core.cpp`, `register_type_and_char_primitives`, `integer?`: `types::make_bool(types::is_int(a[0]))`, so any float is rejected.
- `inexact->exact` is registered in `evaluator_primitives_math.cpp` next to `floor` / `ceil` / `round` / `trunc`; there is no `exact->inexact`, `exact`, `inexact`, `exact?`, `inexact?`, `truncate` or `ceiling` in `src/compiler` or `lib/std`.

## Expected

- `round` rounds halves to even.
- `integer?` is `#t` for finite floats with no fractional part.
- `exact->inexact` / `inexact` (int → float), `exact` (alias of `inexact->exact`), `exact?` / `inexact?`, `truncate` (alias of `trunc`) and `ceiling` (alias of `ceil`) exist, or calling them gives an error that names the Aura spelling.

## Acceptance

- The repro prints the expected values.
- Tests for `round` at ±0.5, ±1.5, ±2.5, and for `integer?` on `2`, `2.0`, `2.5`, `(floor 2.7)`.
