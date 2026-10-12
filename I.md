**Filed from:** cybrid-systems/aura-rl-sutton (Aura port of the Sutton & Barto RL algorithms)

## Summary

Division by zero gives different results depending on whether the divisor is a literal:

- `(/ 1.0 0.0)` and `(/ 1 0)` written with a literal zero report `error: division by zero`.
- The same division with the zero coming from a variable, a parameter, a `vector-ref` or an expression returns the integer `0`, with no message, and the program goes on.

So `(/ sum count)` with `count = 0`, or an importance-sampling ratio with a zero denominator, quietly becomes `0` and corrupts the numbers that follow. Float division does not follow IEEE either (`1.0/0.0` should be `+inf`, `0.0/0.0` NaN), although other float primitives already return IEEE specials: `(log 0.0)` → `-inf`, `(sqrt -1.0)` → `nan`, `(* 1e308 10.0)` → `inf`.

Aura `main` at `2f815c188`. Same output on the Soft face (`AURA_SANDBOX=off AURA_PIPELINE_STRICT=0`) and on the default face, file mode (`aura file.aura`).

## Repro

```scheme
; div0.aura
(define (r a b) (/ a b))
(display (r 1.0 0.0)) (newline)                          ; 0
(display (r 1 0)) (newline)                              ; 0
(let ((a 1.0) (b 0.0)) (display (/ a b))) (newline)     ; 0
(define b 0.0) (display (/ 1.0 b)) (newline)            ; 0
(display (r 1.0 (- 0.5 0.5))) (newline)                  ; 0
(define (f v) (/ (vector-ref v 0) (vector-ref v 1)))
(display (f (vector 3.0 0.0))) (newline)                 ; 0
(define x (r 1.0 0.0))
(display (number? x)) (display (= x 0)) (newline)        ; #t#t
(display "after") (newline)
(display (/ 1.0 0.0)) (newline)                          ; error: division by zero
```

```text
$ aura div0.aura; echo rc=$?
0
0
0
0
0
0
#t#t
after
error: division by zero: division by zero
  use a non-zero denominator
rc=1
```

For comparison, `(modulo a b)` with a zero `b` from a parameter returns an error value (`<error>`), not `0`.

## Cause (code)

`src/compiler/evaluator_primitives_builtins.cpp`, the `table_["/"]` primitive: `arithmetic_div_pure` (`src/compiler/evaluator_pure.ixx`) returns `std::unexpected(DivisionByZero)`, and the primitive maps every error to `make_int(0)`:

```cpp
// we mirror the legacy behavior (silent 0 result for non-empty divisor
// lists, or 0 for the reciprocal case) so the existing test surface
// doesn't change. A future migration can surface the error.
...
if (a.empty()) return make_int(1);
return make_int(0);
```

The literal case takes a different path (constant folding skips a zero divisor, and the IR executor `IROpcode::Div` in `src/compiler/ir_executor_impl.cpp` returns a `DivisionByZero` diagnostic), so the two paths disagree.

## Expected

The same result for literal and non-literal divisors. Either:

- float division by zero follows IEEE 754 (`(/ 1.0 0.0)` → `+inf`, `(/ -1.0 0.0)` → `-inf`, `(/ 0.0 0.0)` → `nan`), matching `log` / `sqrt` / overflow, and integer division by zero returns the primitive error value like `modulo` / `quotient`; or
- every division by zero is an error, in both paths.

In no case should a division by zero produce a normal-looking `0`.

## Workaround in aura-rl-sutton

The code guards every division whose denominator can be zero (visit counts, importance-sampling weight sums) with an explicit `(if (> n 0) ... default)`.
