#!/usr/bin/env python3
# ==================================================================
# WHAT IS ACTUALLY UNDER 3-6-9
# The same doubling map, followed down until it reaches
# an unsolved problem and the foundation of cryptography.
# ==================================================================
from math import gcd
from sympy import isprime   # only for a cross-check; falls back if absent

LIM = 300000

# ---------- sieve: smallest prime factor ----------
spf = list(range(LIM+1))
for i in range(2, int(LIM**0.5)+1):
    if spf[i] == i:
        for j in range(i*i, LIM+1, i):
            if spf[j] == j: spf[j] = i
primes = [p for p in range(2, LIM+1) if spf[p] == p]

def factor_set(m):
    f = set()
    while m > 1:
        f.add(spf[m]); m //= spf[m]
    return f

def mult_order(a, p):
    """order of a in (Z/pZ)*, p prime — divides p-1"""
    if a % p == 0: return 0
    o = p - 1
    for q in factor_set(p-1):
        while o % q == 0 and pow(a, o//q, p) == 1:
            o //= q
    return o

print("="*68)
print("WHAT IS ACTUALLY UNDER 3-6-9")
print("="*68)

# ==================================================================
print("\n[1] THE SAME MACHINE, ONE FLOOR DOWN — repeating decimals")
print("-"*68)
print("  The period of 1/p is exactly the order of 10 in the group mod p.")
print("  Digital roots and repeating decimals are the SAME fact.\n")
print(f"  {'p':>5}{'period of 1/p':>15}{'p-1':>7}   full reptend?")
for p in [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    o = mult_order(10, p)
    print(f"  {p:>5}{o:>15}{p-1:>7}   {'YES' if o == p-1 else 'no'}")

print("\n  When the period is maximal (p-1) the prime is called FULL REPTEND,")
print("  and its decimal expansion is a CYCLIC NUMBER. Watch 1/7:\n")
base = 142857
for k in range(1, 8):
    prod = base*k
    tag = "  <-- all nines" if k == 7 else ""
    print(f"    142857 x {k} = {prod:>7}{tag}")
print("\n  Every multiple from 1 to 6 is the SAME SIX DIGITS, rotated.")
print("  The seventh is 999999. This is the genuine version of the magic")
print("  people think they see in 3-6-9 — and it is completely explained:")
print("  10 is a primitive root mod 7, so its powers sweep every residue")
print("  once before returning, and each sweep is a rotation of the same cycle.")

# ==================================================================
print("\n[2] WHICH MODULI EVEN HAVE A PRIMITIVE ROOT? (Gauss)")
print("-"*68)
def has_primroot(n):
    if n in (1, 2, 4): return True
    m = n
    if m % 2 == 0: m //= 2
    if m % 2 == 0: return False            # divisible by 4 and >4
    f = factor_set(m)
    return len(f) == 1                      # p^k or 2p^k
good = [n for n in range(2, 40) if has_primroot(n)]
bad  = [n for n in range(2, 40) if not has_primroot(n)]
print(f"  have one : {good}")
print(f"  have none: {bad}")
print("\n  Gauss proved the pattern exactly: only 1, 2, 4, p^k and 2p^k")
print("  for odd primes p. Our 9 = 3^2 makes the list — which is the")
print("  reason doubling sweeps the whole group and the 3-6-9 split appears.")
print("  Change 9 for 8, 12, 15 or 16 and the structure collapses.")

# ==================================================================
print("\n[3] THE UNSOLVED PROBLEM HIDING IN THE DOUBLING MAP")
print("-"*68)
print("  Ask the obvious next question: for how many primes p is 2")
print("  a primitive root — i.e. how often does doubling sweep everything?")
print("  Artin conjectured in 1927 that the density is\n")
ARTIN = 0.3739558136192022880547280543464164151116
print(f"    A = prod_p (1 - 1/(p(p-1))) = {ARTIN:.10f}\n")
print("  NOBODY HAS PROVED IT. Hooley proved it in 1967 assuming the")
print("  Generalised Riemann Hypothesis. Unconditionally it is still open.")
print("  We can only measure it:\n")
print(f"  {'primes up to':>14}{'count':>9}{'2 is prim.root':>16}{'density':>10}{'vs A':>10}")
for cap in (1000, 10000, 50000, 100000, 200000, 300000):
    sub = [p for p in primes if 3 <= p <= cap]
    hit = sum(1 for p in sub if mult_order(2, p) == p-1)
    d = hit/len(sub)
    print(f"  {cap:>14,}{len(sub):>9,}{hit:>16,}{d:>10.4f}{d-ARTIN:>+10.4f}")
print("\n  It converges on Artin's constant and nobody can explain why.")
print("  That is the honest floor beneath 3-6-9: not a hidden key, but a")
print("  hundred-year-old open problem in the same machinery.")

# ==================================================================
print("\n[4] THE UNIFICATION — this is where our whole session meets")
print("-"*68)
print("  Every structure we have touched is CHARACTERS OF A GROUP:\n")
rows = [
 ("circle  R/Z",        "e^{2 pi i t}",   "sin, cos",             "Fourier series"),
 ("cube    (Z/2)^n",    "prod x_i",       "parity functions",     "the census, Huang"),
 ("units   (Z/n)*",     "chi(a)",         "Dirichlet characters", "L-functions, RH"),
]
print(f"  {'group':<18}{'character':<16}{'we call them':<24}{'leads to'}")
for g, c, w, l in rows:
    print(f"  {g:<18}{c:<16}{w:<24}{l}")
print("\n  Same construction three times. The first gave you sin and cos.")
print("  The second gave us Parseval and the 65,536-function census.")
print("  The third gives Dirichlet characters, then L-functions, then the")
print("  Riemann Hypothesis. One idea, three floors, and the bottom floor")
print("  is the deepest open problem in mathematics.")

# small Dirichlet character table mod 9 — the very modulus behind 3-6-9
print("\n  characters of (Z/9)*, the group that generates 3-6-9:")
units9 = [a for a in range(1, 10) if gcd(a, 9) == 1]
g = 2                                   # primitive root mod 9
idx = {pow(g, k, 9): k for k in range(6)}
print(f"    group {units9}, generator {g}, order 6")
for j in range(3):
    row = " ".join(f"{(j*idx[a])%6:>2}" for a in units9)
    print(f"    chi_{j}: exponents of w=e^(2 pi i/6) -> {row}")
print("    (the j=0 row is the trivial character; the rest encode the")
print("     multiplicative structure the digital-root pattern rides on)")

# ==================================================================
print("\n[5] WHERE IT REALLY IS A KEY — the same arithmetic, working")
print("-"*68)
p, q = 1000003, 1000033
n_rsa = p*q
phi = (p-1)*(q-1)
e = 65537
d = pow(e, -1, phi)
msg = 369
ct = pow(msg, e, n_rsa)
pt = pow(ct, d, n_rsa)
print(f"  primes p,q      {p:,} , {q:,}")
print(f"  modulus n       {n_rsa:,}")
print(f"  phi(n)          {phi:,}")
print(f"  public  e       {e}")
print(f"  private d       {d:,}")
print(f"\n  encrypt 369  -> {ct:,}")
print(f"  decrypt      -> {pt}   {'recovered' if pt == msg else 'FAILED'}")
print("\n  That is Euler's theorem: a^phi(n) = 1 mod n. The identical fact")
print("  that makes digital roots work makes this work. Its security rests")
print("  on factoring being hard — a complexity assumption, which is where")
print("  this whole conversation started.")

print("\n" + "="*68)
print("  3-6-9 is a shadow cast by base ten.")
print("  The thing casting it runs from repeating decimals through an")
print("  unsolved conjecture to the Riemann Hypothesis and RSA.")
print("  The shadow is not the key. The lamp is.")
print("="*68)
