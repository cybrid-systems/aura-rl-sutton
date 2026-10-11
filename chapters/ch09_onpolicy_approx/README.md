# Chapter 9 — On-policy Prediction with Approximation

Status: stub

Algorithms / experiments to reimplement in Aura:

- gradient MC with state aggregation, 1000-state walk (Fig 9.1)
- semi-gradient TD(0) (Fig 9.2)
- polynomial vs Fourier bases (Fig 9.5)
- coarse coding (Fig 9.8)
- tile coding (Fig 9.10)

Reference implementation (Python, for cross-checking numbers only): `chapter09/random_walk.py, square_wave.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 9`
