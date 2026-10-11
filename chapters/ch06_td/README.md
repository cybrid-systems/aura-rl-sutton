# Chapter 6 — Temporal-Difference Learning

Status: stub (envs ready: `lib/envs/random-walk.aura`, `lib/envs/cliffwalking.aura`)

Algorithms / experiments to reimplement in Aura:

- TD(0) vs constant-α MC on the random walk (Ex 6.2)
- batch updating (Fig 6.2)
- Sarsa on the windy gridworld (Ex 6.5)
- Q-learning vs Sarsa vs Expected Sarsa on cliff walking (Ex 6.6)
- Double Q-learning and maximization bias (Fig 6.7)

Reference implementation (Python, for cross-checking numbers only): `chapter06/random_walk.py, windy_grid_world.py, cliff_walking.py, maximization_bias.py` in
[ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction).
Code here is written from the book's pseudocode; no code or prose is copied.

Run: `scripts/run_chapter.sh 6`
