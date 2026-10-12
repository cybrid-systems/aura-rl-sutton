**Filed from:** cybrid-systems/aura-rl-sutton (Aura port of the Sutton & Barto RL algorithms)

## Summary

`display` and `write` do not print the value for two common cases:

- **Vectors** print as `<vector[N]>`, where `N` is the vector's heap slot index, not its length or contents. `(display (vector 1 2 3))` prints `<vector[0]>`. Two different vectors of different sizes can print the same way in two runs, and the number changes when unrelated code allocates a vector first.
- **Floats** print with `%g`, which keeps 6 significant digits. `(display 0.1234567891)` prints `0.123457` and `(display 123456789.25)` prints `1.23457e+08`. `number->string` on the same values gives `0.1234567891` and `123456789.25`, so `display`, `write` and `number->string` disagree. Because `write` is also affected, written data cannot be read back exactly.

In the RL port, every result table has to go through `number->string` (or a rounding helper) and every vector has to be printed element by element. Printing a learned parameter vector with `display` while debugging shows only `<vector[12]>`, and printing a step size `2^-13` shows `0.00012207`.

Aura `main` at `3034d4723` (RelWithDebInfo), file mode, Soft face (`AURA_SANDBOX=off AURA_PIPELINE_STRICT=0`). Same output at `5cc915687`.

## Repro

```scheme
(define v (vector 1 2 3))
(display v) (newline)
(write v) (newline)
(display (list 1 v)) (newline)
(display (make-vector 2 0.5)) (newline)
(define x 0.1234567891)
(display x) (newline)
(write x) (newline)
(display (number->string x)) (newline)
(display 123456789.25) (newline)
(display (list 0.0001220703125 2.5)) (newline)
```

Output, exit 0:

```text
<vector[0]>
<vector[0]>
(1 <vector[0]>)
<vector[1]>
0.123457
0.123457
0.1234567891
1.23457e+08
(0.00012207 2.5)
```

Expected (R7RS `display` / `write`):

```text
#(1 2 3)
#(1 2 3)
(1 #(1 2 3))
#(0.5 0.5)
0.1234567891
0.1234567891
0.1234567891
123456789.25
(0.0001220703125 2.5)
```

## Where

- `src/compiler/evaluator_primitives_runtime.cpp`, `io_print_val`: `std::fprintf(stdout, "<vector[%zu]>", (size_t)as_vector_idx(v));` for vectors and `std::fprintf(stdout, "%g", as_float(v));` for floats.
- The same file, `fmt_val_to_string`: `std::format("<vector[{}]>", as_vector_idx(v))` and `std::to_string(as_float(v))` (6 fixed decimals, so `1e-9` becomes `0.000000`).
- `src/compiler/value.ixx` and `src/compiler/evaluator.ixx` have the same `<vector[{}]>` formatting.
- Hash tables already print their occupancy instead of the index (#3916); vectors were left with the index.

## Expected

- Vectors print their elements, `#(e1 e2 ...)`, recursing with the same depth limit as lists.
- Floats print with the shortest representation that reads back to the same double (for example `std::to_chars` without a precision), in `display`, `write`, `fmt_val_to_string` and `number->string` alike.

## Acceptance

- The repro prints the expected block above.
- A regression test checks that `(string->number (number->string x))`, and reading back what `write` prints, return `x` exactly for a few doubles (`0.1`, `2^-13`, `1e-9`, `123456789.25`, `(/ 1.0 3.0)`).
