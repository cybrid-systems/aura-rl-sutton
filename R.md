**Filed from:** cybrid-systems/aura-rl-sutton (Aura port of the Sutton & Barto RL algorithms)

## Summary

`eqv?` has no runtime primitive. On the Soft face every call is `unbound variable: eqv?` (hint: "did you mean 'e'?"), at top level and inside procedures. The IR lowering does know the name and maps it to `IROpcode::Eq`, so `eqv?` only works on a path that lowers the call to IR and fails on the tree-walker. `memv` and `assv`, the list operations built on `eqv?`, are also unbound.

R7RS specifies `case`, `memv` and `assv` in terms of `eqv?`, and code ported from Scheme uses it, so it fails as soon as it runs on the tree-walker. In the RL port we use `equal?` everywhere instead (`eq?` has its own problem with symbols, #4455).

Aura `main` at `3034d4723` (RelWithDebInfo), file mode. Same at `5cc915687`.

## Repro

```scheme
(display (eq? 'a 'a)) (newline)
(display (eqv? 2 2)) (newline)
(display "after") (newline)
```

Soft (`AURA_SANDBOX=off AURA_PIPELINE_STRICT=0`), exit 1:

```text
#t
error: 2:11: unbound variable: eqv?
  did you mean 'e'?
   |
  2 | (display (eqv? 2 2)) (newline)
   |           ^^^^
after
```

Inside a procedure, `(define (f a b) (eqv? a b)) (display (f 2 2))`, the error is the same, at the `eqv?` in the body.

## Where

- `src/compiler/lowering_impl.cpp`, the `kPrimOps` table: `{"eqv?", IROpcode::Eq}` next to `{"eq?", IROpcode::Eq}`.
- `src/compiler/macro_expansion.cpp` lists `"eqv?"` among the known primitive names, and `evaluator_primitives_mutate.cpp` lists it in its primitive-name tables.
- No `add("eqv?", ...)` / `register_prim(..., "eqv?", ...)` exists in `src/compiler`, and `lib/std` does not define `eqv?`, `memv` or `assv`.

## Expected

- `eqv?` is a runtime primitive with R7RS semantics: `eq?` plus numeric equality for two numbers of the same exactness (`(eqv? 2 2)` → `#t`, `(eqv? 2 2.0)` → `#f`, `(eqv? 1.5 1.5)` → `#t`) and character equality. The tree-walker and the IR `Eq` lowering give the same answer; if `Eq` is pointer/fixnum equality, floats need their own check before lowering `eqv?` to it.
- `memv` and `assv` exist.

## Acceptance

- The repro prints `#t`, `#t`, `after` and exits 0.
- A test runs `eqv?` on ints, floats, symbols and characters on both the tree-walker and the lowered path and checks that they agree.
