#!/usr/bin/env python3
# ==================================================================
# THE PROFILE SOLVER
#
# Our construction "some residue class is empty" gives max(d, n/d).
# But at n = 10 and n = 14 the true floor is LOWER, so something beats
# it -- and we did not know what.
#
# Key move: run the exact solver on the PROFILE GRAPH instead of the
# necklace graph. Profiles number in the hundreds where necklaces
# number in the millions. That makes the optimum over the whole
# residue family exactly computable at sizes search cannot touch.
#
# Then ask the real question: is the true optimum ALWAYS a residue
# function? If so we have a structural conjecture worth stating.
# ==================================================================
import sys, itertools, math, time
sys.setrecursionlimit(400000)

def canon(c):
    d = len(c)
    return min(tuple(c[k:] + c[:k]) for k in range(d))

def profile_graph(d, m):
    """nodes = canonical profiles; edge weight c->c' = how many single-bit
       flips at a point with profile c land on profile c'.
       Weights are DIRECTIONAL, as in the necklace graph."""
    nodes = sorted({canon(c) for c in itertools.product(range(m+1), repeat=d)})
    index = {p: i for i, p in enumerate(nodes)}
    fwd = []
    for c in nodes:
        acc = {}
        for r in range(d):
            if c[r] > 0:
                t = list(c); t[r] -= 1
                k = index[canon(tuple(t))]
                acc[k] = acc.get(k, 0) + c[r]          # c_r ones to flip down
            if c[r] < m:
                t = list(c); t[r] += 1
                k = index[canon(tuple(t))]
                acc[k] = acc.get(k, 0) + (m - c[r])    # m-c_r zeros to flip up
        fwd.append(acc)
    return nodes, fwd

def solve_profile(d, m, t, budget=4_000_000):
    """EXACT: is there a non-constant mod-d profile function with s <= t?"""
    nodes, fwd = profile_graph(d, m)
    K = len(nodes)
    seen = [False]*K; order = []; q = [0]; seen[0] = True
    while q:
        j = q.pop(0); order.append(j)
        for k in fwd[j]:
            if not seen[k]: seen[k] = True; q.append(k)
    for j in range(K):
        if not seen[j]: order.append(j)

    val, diff = [-1]*K, [0]*K
    nodes_used = [0]; hit = [None]; trail = []

    def assign(j0, b0, tr):
        st = [(j0, b0)]
        while st:
            j, b = st.pop()
            if val[j] != -1:
                if val[j] != b: return False
                continue
            val[j] = b; tr.append(('v', j, 0))
            for k, w in fwd[j].items():
                if k == j: continue
                if val[k] != -1 and val[k] != b:
                    diff[j] += w; tr.append(('d', j, w))
                    if diff[j] > t: return False
                    wk = fwd[k].get(j, 0)
                    diff[k] += wk; tr.append(('d', k, wk))
                    if diff[k] > t: return False
            for c in (j,) + tuple(fwd[j].keys()):
                if val[c] != -1 and diff[c] == t:
                    for k2 in fwd[c]:
                        if k2 != c and val[k2] == -1: st.append((k2, val[c]))
        return True

    def undo(tr, mk):
        while len(tr) > mk:
            kd, i, w = tr.pop()
            if kd == 'v': val[i] = -1
            else: diff[i] -= w

    def dfs(i):
        nodes_used[0] += 1
        if nodes_used[0] > budget: return "B"
        while i < K and val[order[i]] != -1: i += 1
        if i == K:
            if any(v == 1 for v in val) and any(v == 0 for v in val):
                hit[0] = val[:]; return True
            return False
        j = order[i]
        for b in (0, 1):
            mk = len(trail)
            if assign(j, b, trail):
                r = dfs(i+1)
                if r == "B": undo(trail, mk); return "B"
                if r: return True
            undo(trail, mk)
        return False
    r = dfs(0)
    return (r is True), (r != "B"), K, hit[0], nodes

def family_floor(n, d):
    m = n // d
    for t in range(1, n+1):
        sat, fin, K, w, nodes = solve_profile(d, m, t)
        if not fin: return None, K
        if sat: return t, K
    return None, None

print("="*74)
print("EXACT OPTIMA OVER THE RESIDUE-PROFILE FAMILY")
print("="*74)

# ------------------------------------------------------------------
print("\n[1] CALIBRATION — must reproduce what we already proved")
print("-"*74)
known_family = {(9,3):3, (10,2):4, (6,2):3, (6,3):3, (8,2):4}
print(f"  {'n':>4}{'d':>3}{'profiles':>10}{'solver':>8}{'expected':>10}{'':>4}")
bad = 0
for (n, d), exp in sorted(known_family.items()):
    f, K = family_floor(n, d)
    ok = (f == exp); bad += (not ok)
    print(f"  {n:>4}{d:>3}{K:>10}{str(f):>8}{exp:>10}{'OK' if ok else 'MISMATCH':>4}")
if bad:
    print("\n  calibration failed — stopping."); raise SystemExit

# ------------------------------------------------------------------
print("\n[2] THE FAMILY OPTIMUM vs OUR EARLIER CONSTRUCTION")
print("-"*74)
print("  'construction' = the simple rule max(d, n/d).")
print("  'family best'  = the BEST profile function, found exactly.\n")
print(f"  {'n':>4}{'d':>3}{'profiles':>10}{'construction':>14}"
      f"{'family best':>13}{'improved?':>11}")
print("  " + "-"*58)
fam = {}
for n in (6, 8, 9, 10, 12, 14, 15, 16, 18, 20):
    for d in [x for x in range(2, n) if n % x == 0]:
        m = n//d
        if (m+1)**d > 2_000_000: continue
        f, K = family_floor(n, d)
        if f is None: continue
        simple = max(d, m)
        fam.setdefault(n, []).append((d, f))
        mark = f"YES ({simple}->{f})" if f < simple else ""
        print(f"  {n:>4}{d:>3}{K:>10}{simple:>14}{f:>13}{mark:>11}")

# ------------------------------------------------------------------
print("\n[3] THE CONJECTURE THIS SUGGESTS")
print("-"*74)
# ONLY values we exhaustively proved. n=15,18,20 were bracketed, never
# pinned, so they must not be used as if they were established.
floors = {6:3, 8:4, 9:3, 10:4, 12:4, 14:4, 16:4,
          15:None, 18:None, 20:None}
print(f"  {'n':>4}{'best d':>8}{'family floor':>14}{'true floor':>12}{'equal?':>9}")
print("  " + "-"*48)
agree = miss = 0
for n in sorted(fam):
    d, f = min(fam[n], key=lambda p: p[1])
    tf = floors.get(n)
    if tf is None:
        print(f"  {n:>4}{d:>8}{f:>14}{'unknown':>12}{'-':>9}")
        continue
    eq = (f == tf)
    agree += eq; miss += (not eq)
    print(f"  {n:>4}{d:>8}{f:>14}{tf:>12}{('YES' if eq else 'no'):>9}")

print(f"""
  Agreements: {agree}   Disagreements: {miss}

  If that second number is zero, then every composite n we can check has
  its optimum attained by a RESIDUE-PROFILE function -- a family whose
  description is a few hundred numbers regardless of how big n gets.

  That is a genuine structural statement, and it is testable: a single
  composite n whose true floor beats every profile function would kill it.
""")

# ------------------------------------------------------------------
print("[4] WHERE SEARCH CANNOT GO — exact family optima at large n")
print("-"*74)
print("  These are EXACT over the family, at sizes with millions of")
print("  necklaces and hundreds of millions of inputs.\n")
print(f"  {'n':>5}{'d':>4}{'profiles':>10}{'inputs':>14}{'family floor':>14}"
      f"{'simple rule':>13}")
print("  " + "-"*60)
for n, d in ((24,4),(24,6),(25,5),(26,2),(26,13),(27,3),(27,9),(36,6),(49,7)):
    m = n//d
    if (m+1)**d > 400_000:
        print(f"  {n:>5}{d:>4}{'too big':>10}"); continue
    t0 = time.time()
    f, K = family_floor(n, d)
    print(f"  {n:>5}{d:>4}{K:>10}{'2^'+str(n):>14}{str(f):>14}{max(d,m):>13}")

print("""
  Compare the last two columns. Wherever they differ, the simple
  "some class is empty" rule was NOT the best member of its own family,
  and the solver found the better one.
""")
print("="*74)
