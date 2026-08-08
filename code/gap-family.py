#!/usr/bin/env python3
# ==================================================================
# THE GAP FAMILY — closing the prime hole
#
# The residue construction needs a proper divisor, so it is EMPTY at
# prime n. Yet primes have low floors (n=5,7 -> 3; n=11 -> 4) achieved
# by something we could not describe.
#
# Second natural invariant, available for EVERY n:
#   list the gaps between consecutive ones around the cycle and take
#   the MULTISET. Rotating the input permutes the gaps, so any function
#   of that multiset is cyclically invariant.
#
# Unlike residues this exists at primes. Does it reach their floors?
# ==================================================================
import sys, time
sys.setrecursionlimit(200000)

def rot(x, k, n):
    return ((x << k) | (x >> (n-k))) & ((1 << n) - 1)

def structure(n):
    N = 1 << n
    orb = {}
    for x in range(N):
        o = min(rot(x, k, n) for k in range(n))
        orb.setdefault(o, []).append(x)
    necks = sorted(orb)
    idx = {}
    for j, o in enumerate(necks):
        for x in orb[o]: idx[x] = j
    nb = [[idx[o ^ (1 << i)] for i in range(n)] for o in necks]
    return necks, nb

def gap_multiset(o, n):
    """sorted tuple of cyclic gaps between consecutive ones"""
    ones = [i for i in range(n) if o >> i & 1]
    if not ones: return ("empty",)
    if len(ones) == n: return tuple([0]*n)
    gaps = []
    for a in range(len(ones)):
        b = (a + 1) % len(ones)
        g = (ones[b] - ones[a] - 1) % n
        gaps.append(g)
    return tuple(sorted(gaps))

def solve_family(n, t, groupfn, budget=6_000_000):
    """EXACT: is there a non-constant cyclically invariant f on n bits,
       CONSTANT on each group, with sensitivity <= t?
       Variables are groups; constraints live on necklaces."""
    necks, nb = structure(n)
    K = len(necks)
    gid, groups = {}, []
    gof = []
    for j in range(K):
        key = groupfn(necks[j], n)
        if key not in gid:
            gid[key] = len(groups); groups.append(key)
        gof.append(gid[key])
    G = len(groups)

    # for each necklace j: neighbour groups with multiplicity
    ncon = []
    for j in range(K):
        d = {}
        for k in nb[j]: d[gof[k]] = d.get(gof[k], 0) + 1
        ncon.append((gof[j], d))
    # which necklace-constraints touch each group
    touch = [[] for _ in range(G)]
    for j, (gj, d) in enumerate(ncon):
        for g in set([gj] + list(d)): touch[g].append(j)

    val = [-1]*G
    nodes = [0]; hit = [None]

    def viol(j):
        """current forced disagreement count at necklace j; None if unknown"""
        gj, d = ncon[j]
        if val[gj] == -1: return 0
        s = 0
        for g, m in d.items():
            if val[g] != -1 and val[g] != val[gj]: s += m
        return s

    order = sorted(range(G), key=lambda g: -len(touch[g]))

    def dfs(i):
        nodes[0] += 1
        if nodes[0] > budget: return "B"
        if i == G:
            if any(v == 1 for v in val) and any(v == 0 for v in val):
                hit[0] = val[:]; return True
            return False
        g = order[i]
        for b in (0, 1):
            val[g] = b
            ok = True
            for j in touch[g]:
                if viol(j) > t: ok = False; break
            if ok:
                r = dfs(i+1)
                if r == "B": val[g] = -1; return "B"
                if r: return True
            val[g] = -1
        return False

    r = dfs(0)
    return (r is True), (r != "B"), G, K

def family_floor(n, groupfn):
    for t in range(1, n+1):
        sat, fin, G, K = solve_family(n, t, groupfn)
        if not fin: return None, G, K
        if sat: return t, G, K
    return None, None, None

print("="*74)
print("THE GAP FAMILY")
print("="*74)
print("""
  A gap function depends only on the MULTISET of spacings between the
  ones. It exists for every n, primes included, and the number of
  multisets is roughly the number of integer partitions of n -- far
  smaller than the number of necklaces.
""")

floors = {5:3, 6:3, 7:3, 8:4, 9:3, 10:4, 11:4, 12:4, 13:None, 14:4, 16:4}

print(f"  {'n':>4}{'prime?':>8}{'necklaces':>11}{'gap groups':>12}"
      f"{'gap floor':>11}{'true floor':>12}{'attains it?':>13}")
print("  " + "-"*68)
res = {}
for n in range(5, 17):
    isp = all(n % d for d in range(2, n))
    t0 = time.time()
    f, G, K = family_floor(n, gap_multiset)
    tf = floors.get(n)
    res[n] = f
    if f is None:
        print(f"  {n:>4}{str(isp):>8}{'--':>11}{'--':>12}{'timeout':>11}"
              f"{str(tf):>12}{'--':>13}")
        continue
    verdict = ("YES" if tf is not None and f == tf else
               ("NO" if tf is not None else "?"))
    print(f"  {n:>4}{str(isp):>8}{K:>11}{G:>12}{f:>11}{str(tf):>12}{verdict:>13}")

print("\n[2] THE PRIMES SPECIFICALLY")
print("-"*74)
primes = [n for n in res if all(n % d for d in range(2, n)) and res[n]]
hit = [n for n in primes if floors.get(n) == res[n]]
print(f"  primes tested   : {primes}")
print(f"  gap family value: {[res[n] for n in primes]}")
print(f"  true floor      : {[floors.get(n) for n in primes]}")
print(f"  attained at     : {hit}")
print("""
  If the gap family reaches the prime floors, the hole is closed: every
  n is covered by one of two elementary families -- residues when n
  factors, gaps when it does not.

  If it does NOT, then primes are genuinely harder and the thing that
  achieves their floor is still undescribed. Either answer is worth
  having, and the table above decides it.
""")
print("="*74)
