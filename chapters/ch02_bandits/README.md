# Chapter 2 — Multi-armed Bandits

Status: partial: Fig 2.2–2.5 run (`ten_armed_testbed.aura`)

Algorithms / experiments to reimplement in Aura:

- ε-greedy with sample averages (Fig 2.2)
- optimistic initial values, constant step α (Fig 2.3)
- UCB action selection (Fig 2.4)
- gradient bandit with/without baseline (Fig 2.5)
- parameter study (Fig 2.6) — TODO

Reference implementation (Python, for cross-checking numbers only): `chapter02/ten_armed_testbed.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 2`
