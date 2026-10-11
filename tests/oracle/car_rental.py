#!/usr/bin/env python3
"""Jack's car rental (Example 4.2) by policy iteration with the full Poisson model
(requests 3/4, returns 3/2, tails cut at 25), for chapters/ch04_dp/car_rental.aura.
Evaluation is synchronous to theta = 1e-4 and improvement keeps the old action
unless another is better by more than 1e-9, as in lib/envs/car-rental.aura.
The two locations are independent given the cars after the move, so the expected
next value is R1 + R2 + gamma * T1 V T2^T with numpy matrices."""
import numpy as np
from math import exp, factorial

N, K, G = 21, 25, 0.9

def pois(lam):
    return np.array([exp(-lam) * lam ** k / factorial(k) for k in range(K + 1)])

def location(lreq, lret):
    pr, pt = pois(lreq), pois(lret)
    T, R = np.zeros((N, N)), np.zeros(N)
    for n in range(N):
        for k in range(K + 1):
            rented = min(k, n)
            R[n] += pr[k] * 10 * rented
            for j in range(K + 1):
                T[n, min(20, n - rented + j)] += pr[k] * pt[j]
    return T, R

T1, R1 = location(3, 3)
T2, R2 = location(4, 2)

def table(V):
    return R1[:, None] + R2[None, :] + G * T1 @ V @ T2.T

def q(E, i, j, a):
    return E[min(20, i - a), min(20, j + a)] - 2 * abs(a)

V = np.zeros((N, N)); pol = np.zeros((N, N), dtype=int); rounds = 0
while True:
    sweeps = 0
    while True:
        sweeps += 1
        E = table(V)
        newV = np.array([[q(E, i, j, pol[i, j]) for j in range(N)] for i in range(N)])
        d = np.abs(newV - V).max(); V = newV
        if d < 1e-4:
            break
    E = table(V); changed = 0
    for i in range(N):
        for j in range(N):
            old = pol[i, j]; best, bq = old, q(E, i, j, old) + 1e-9
            for a in range(-5, 6):
                if a <= i and -a <= j and q(E, i, j, a) > bq:
                    best, bq = a, q(E, i, j, a)
            pol[i, j] = best; changed += best != old
    print(f"round {rounds} sweeps={sweeps} changed={changed}")
    if changed == 0:
        break
    rounds += 1
print("v(0,0)=%.6f v(20,20)=%.6f v(10,10)=%.6f v(20,0)=%.6f v(0,20)=%.6f" % (V[0, 0], V[20, 20], V[10, 10], V[20, 0], V[0, 20]))
print("V min %.4f max %.4f" % (V.min(), V.max()))
for i in (20, 15, 10, 5, 4, 0):
    print(i, " ".join(str(int(x)) for x in pol[i]))

# Small-case numbers for tests/test_ch04_dp_examples.aura: from V = 0 and the
# all-zero policy, 10 evaluation sweeps, then one greedy improvement.
V = np.zeros((N, N)); pol = np.zeros((N, N), dtype=int)
for _ in range(10):
    E = table(V)
    V = np.array([[q(E, i, j, 0) for j in range(N)] for i in range(N)])
print("10 sweeps: v(0,0)=%.6f v(20,20)=%.6f v(5,15)=%.6f" % (V[0, 0], V[20, 20], V[5, 15]))
E = table(V); changed = 0
for i in range(N):
    for j in range(N):
        best, bq = 0, q(E, i, j, 0) + 1e-9
        for a in range(-5, 6):
            if a <= i and -a <= j and q(E, i, j, a) > bq:
                best, bq = a, q(E, i, j, a)
        pol[i, j] = best; changed += best != 0
print("improve: changed=%d pi(20,0)=%d pi(0,20)=%d pi(10,10)=%d pi(15,3)=%d" % (changed, pol[20, 0], pol[0, 20], pol[10, 10], pol[15, 3]))
print("T1 row 10 sum=%.12f R1[20]=%.6f R2[20]=%.6f R1[0]=%.1f" % (T1[10].sum(), R1[20], R2[20], R1[0]))
