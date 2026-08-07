#!/usr/bin/env python3
# ==================================================================
# THE CENSUS — every Boolean function on 4 variables
#
# Computes the full complexity landscape for all 2^16 = 65,536
# functions, verifies Huang's 2019 Sensitivity Theorem exhaustively,
# and rebuilds Huang's actual proof object from scratch.
#
# Deterministic. Pure SI of the discrete world: exact integers.
# ==================================================================
import numpy as np
from functools import lru_cache
from math import comb, sqrt, isqrt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

n     = 4              # variables
N     = 1 << n         # 16 inputs
TOTAL = 1 << N         # 65,536 functions

print("="*66)
print("THE CENSUS — all Boolean functions on 4 variables")
print("="*66)
print(f"functions to examine: {TOTAL:,}   inputs each: {N}")

# ---------- unpack every function into a bit matrix ----------
tt   = np.arange(TOTAL, dtype=np.uint32)
bits = np.zeros((TOTAL, N), dtype=np.uint8)
for x in range(N):
    bits[:, x] = (tt >> x) & 1

# ---------- 1. SENSITIVITY ----------
# s(f) = max over inputs x of the number of single-bit flips that change f
sens = np.zeros(TOTAL, dtype=np.uint8)
for x in range(N):
    s = np.zeros(TOTAL, dtype=np.uint8)
    for i in range(n):
        s += (bits[:, x ^ (1 << i)] != bits[:, x]).astype(np.uint8)
    np.maximum(sens, s, out=sens)

# ---------- 2. DEGREE (via Fourier / Walsh-Hadamard) ----------
vals = (1 - 2 * bits.astype(np.int8)).astype(np.float64)   # {0,1} -> {+1,-1}
a = vals.copy()
step = 1
while step < N:                                   # in-place FWHT along axis 1
    for i in range(0, N, step << 1):
        for j in range(i, i + step):
            u = a[:, j].copy(); v = a[:, j + step].copy()
            a[:, j] = u + v; a[:, j + step] = u - v
    step <<= 1
coef = a / N                                       # Fourier coefficients

popc = np.array([bin(S).count("1") for S in range(N)], dtype=np.uint8)
nz   = np.abs(coef) > 1e-9
deg  = np.zeros(TOTAL, dtype=np.uint8)
for S in range(N):
    deg = np.where(nz[:, S], np.maximum(deg, popc[S]), deg)

parseval = (coef**2).sum(axis=1)
print(f"\nParseval check across all {TOTAL:,} functions: "
      f"min {parseval.min():.9f}  max {parseval.max():.9f}")

# ---------- 3. BLOCK SENSITIVITY ----------
# bs(f) = max over x of the largest set of DISJOINT blocks that each flip f
SUBSETS = [B for B in range(1, N)]                 # non-empty blocks of coords
def bs_of(f):
    best = 0
    for x in range(N):
        fx = (f >> x) & 1
        flips = [B for B in SUBSETS if ((f >> (x ^ B)) & 1) != fx]
        # max disjoint packing, DP over used-coordinate mask
        dp = np.zeros(N, dtype=np.int8)
        for mask in range(N):
            cur = dp[mask]
            for B in flips:
                if not (B & mask):
                    m2 = mask | B
                    if dp[m2] < cur + 1:
                        dp[m2] = cur + 1
        best = max(best, int(dp.max()))
    return best

# ---------- 4. DECISION TREE DEPTH ----------
@lru_cache(maxsize=None)
def dt_depth(v):                                   # v = tuple of subcube values
    if len(v) == 1 or all(b == v[0] for b in v):
        return 0
    k = len(v).bit_length() - 1
    best = k
    for i in range(k):
        v0 = tuple(v[j] for j in range(len(v)) if not (j >> i) & 1)
        v1 = tuple(v[j] for j in range(len(v)) if      (j >> i) & 1)
        d = 1 + max(dt_depth(v0), dt_depth(v1))
        if d < best: best = d
    return best

# ---------- 5. CERTIFICATE COMPLEXITY ----------
def cert_of(f):
    worst = 0
    for x in range(N):
        fx = (f >> x) & 1
        best = n
        for S in range(N):                         # S = fixed coordinate set
            if bin(S).count("1") >= best: continue
            free = (~S) & (N - 1)
            ok, y = True, x & S
            sub = free
            while True:                            # walk the free subcube
                if ((f >> (y | sub)) & 1) != fx: ok = False; break
                if sub == 0: break
                sub = (sub - 1) & free
            if ok: best = bin(S).count("1")
        worst = max(worst, best)
    return worst

print("\ncomputing block sensitivity, decision-tree depth, certificate complexity ...")
bsv  = np.zeros(TOTAL, dtype=np.uint8)
dtv  = np.zeros(TOTAL, dtype=np.uint8)
crt  = np.zeros(TOTAL, dtype=np.uint8)
for f in range(TOTAL):
    bsv[f] = bs_of(f)
    dtv[f] = dt_depth(tuple(int((f >> x) & 1) for x in range(N)))
    crt[f] = cert_of(f)
    if f % 16384 == 0 and f: print(f"  ... {f:,} done")
print("  ... complete")

# ==================================================================
print("\n" + "="*66)
print("[A] THE LANDSCAPE — exact distributions over all 65,536 functions")
print("="*66)
for name, arr in (("sensitivity s(f)", sens), ("block sens bs(f)", bsv),
                  ("degree deg(f)", deg), ("DT depth D(f)", dtv),
                  ("certificate C(f)", crt)):
    counts = np.bincount(arr, minlength=n+1)
    line = "  ".join(f"{v}:{c:>6,}" for v, c in enumerate(counts))
    print(f"{name:>18} | {line}")

frac_max = (deg == n).sum() / TOTAL
print(f"\nShannon's counting argument, made exact:")
print(f"  functions of FULL degree {n}: {(deg==n).sum():,} of {TOTAL:,} = {frac_max*100:.2f}%")
print(f"  -> hardness is the overwhelming default. This is 'largeness' in")
print(f"     Razborov-Rudich, measured rather than assumed.")

# ==================================================================
print("\n" + "="*66)
print("[B] HUANG'S SENSITIVITY THEOREM (2019), verified on every function")
print("="*66)
print("  claim:  s(f) >= sqrt(deg(f))   for every Boolean f")

viol = 0; tight = []
for f in range(TOTAL):
    d = int(deg[f]); s = int(sens[f])
    if d == 0: continue
    if s * s < d: viol += 1
    if s * s == d or (s == int(np.ceil(sqrt(d))) and d > 1): tight.append(f)
print(f"  functions checked : {TOTAL:,}")
print(f"  VIOLATIONS FOUND  : {viol}")
print(f"  verdict           : {'HOLDS UNIVERSALLY' if viol==0 else 'FAILED'}")

gap = sens.astype(float) - np.sqrt(deg.astype(float))
nz_ = deg > 0
print(f"  slack s - sqrt(deg): min {gap[nz_].min():.4f}  "
      f"mean {gap[nz_].mean():.4f}  max {gap[nz_].max():.4f}")
tightest = np.where(nz_ & (gap <= gap[nz_].min() + 1e-9))[0]
print(f"  functions achieving minimum slack: {len(tightest):,}")

# ---------- known inequality chain, tested rather than trusted ----------
print("\n  the standard chain  s <= bs <= C <= D  , tested exhaustively:")
for lbl, ok in (("s  <= bs", (sens <= bsv).all()),
                ("bs <= C ", (bsv  <= crt).all()),
                ("C  <= D ", (crt  <= dtv).all()),
                ("deg<= D ", (deg  <= dtv).all()),
                ("bs <= deg^2", (bsv <= deg.astype(int)**2).all())):
    print(f"    {lbl} : {'holds' if ok else 'FAILS'}")

sep = int((bsv.astype(int) - sens.astype(int)).max())
print(f"\n  largest s-vs-bs separation at n=4: {sep}")
if sep > 0:
    ex = int(np.argmax(bsv.astype(int) - sens.astype(int)))
    print(f"    witness f = 0x{ex:04X}  (s={sens[ex]}, bs={bsv[ex]}, deg={deg[ex]}, D={dtv[ex]})")

# the first run showed C and bs with identical distributions — is it pointwise?
same = int((crt == bsv).sum())
print(f"\n  UNPLANNED CHECK — C(f) vs bs(f): identical for {same:,} of {TOTAL:,} functions")
if same == TOTAL:
    print(f"    C(f) = bs(f) for EVERY function at n=4.")
    print(f"    In general only bs <= C <= bs^2 is guaranteed; the gap needs")
    print(f"    more room than 4 variables provide. n=4 is too small to see it.")
else:
    d = int((crt.astype(int)-bsv.astype(int)).max())
    w = int(np.argmax(crt.astype(int)-bsv.astype(int)))
    print(f"    they differ; largest gap {d} at f = 0x{w:04X}")

# ==================================================================
print("\n" + "="*66)
print("[C] HUANG'S PROOF OBJECT — built from scratch")
print("="*66)
print("  The proof puts +/- signs on hypercube edges and reads the eigenvalues.")
print("  A_1 = [[0,1],[1,0]] ;  A_k = [[A_{k-1}, I], [I, -A_{k-1}]]")

def huang(k):
    if k == 1: return np.array([[0., 1.], [1., 0.]])
    P = huang(k-1); I = np.eye(P.shape[0])
    return np.block([[P, I], [I, -P]])

A = huang(n)
sq  = A @ A
err = np.abs(sq - n*np.eye(A.shape[0])).max()
ev  = np.linalg.eigvalsh(A)
pos = int((ev >  0.5).sum()); neg = int((ev < -0.5).sum())
print(f"\n  A_{n} is {A.shape[0]}x{A.shape[0]}")
print(f"  A^2 = {n}*I ?          max deviation {err:.2e}   -> {'YES' if err<1e-9 else 'NO'}")
print(f"  eigenvalues           +{sqrt(n):.4f} x{pos}   -{sqrt(n):.4f} x{neg}")
print(f"  every |lambda| = {sqrt(n):.4f} ?  {np.allclose(np.abs(ev), sqrt(n))}")
print(f"\n  Cauchy interlacing then forces: any induced subgraph of the")
print(f"  {N}-vertex hypercube on more than {N//2} vertices has a vertex of")
print(f"  degree >= sqrt({n}) = {sqrt(n):.4f}. That single spectral fact is the")
print(f"  whole theorem. Two pages. A thirty-year open problem.")

# ---------- verify the interlacing consequence directly ----------
print("\n  verifying the graph statement by brute force on random large subsets:")
rng = np.random.RandomState(11)
adj = [[x ^ (1 << i) for i in range(n)] for x in range(N)]
worst = 99; trials = 20000
for _ in range(trials):
    size = rng.randint(N//2 + 1, N + 1)
    sub  = set(rng.choice(N, size=size, replace=False).tolist())
    md   = max(sum(1 for y in adj[x] if y in sub) for x in sub)
    worst = min(worst, md)
print(f"    {trials:,} random subsets of size > {N//2}")
print(f"    minimum max-degree observed: {worst}   (theorem requires >= {sqrt(n):.4f})")
print(f"    -> {'CONSISTENT' if worst >= sqrt(n) else 'CONTRADICTION'}")

# ==================================================================
print("\n" + "="*66)
print("[D] THE BARRIER, MEASURED")
print("="*66)
hi_w = (coef**2)[:, popc >= 3].sum(axis=1)      # Fourier weight on levels >= 3
hard = deg == n
best = (0, -1)
for t in np.arange(0.02, 0.95, 0.01):
    acc = ((hi_w > t) == hard).mean()
    if acc > best[1]: best = (t, acc)
thr, acc = best
det = hi_w > thr
tp = int((det &  hard).sum()); fp = int((det & ~hard).sum())
fn = int((~det &  hard).sum()); tn = int((~det & ~hard).sum())
print(f"  spectral detector: weight on levels >=3 exceeds a threshold.")
print(f"  swept every threshold; BEST is {thr:.2f} at {acc*100:.2f}% accuracy.")
print(f"    correct  {tp+tn:>7,}      missed {fn:,}   false alarms {fp:,}")
print(f"\n  HONEST READING — the crude detector is mediocre, not perfect.")
print(f"  Guessing 'hard' for everything already scores {max(hard.mean(),1-hard.mean())*100:.2f}%,")
print(f"  so it beats the trivial baseline by only {(acc-max(hard.mean(),1-hard.mean()))*100:.2f} points.")
print(f"  A single spectral statistic is a weak proxy for real complexity.")
print(f"  Fourier lower bounds work because they use the WHOLE spectrum's")
print(f"  structure under restriction, not one summary number.")
print(f"\n  But both barrier conditions are met, and measurably:")
print(f"    CONSTRUCTIVE — one transform, {N*int(np.log2(N))} operations, timed in ms")
print(f"    LARGE        — {frac_max*100:.2f}% of all functions are full degree")
print(f"  constructive + large = natural. At n=4 there is no cryptography to")
print(f"  break, so nothing stops it. That is precisely why the barrier is")
print(f"  invisible at this scale and fatal at the next one.")

# ==================================================================  plots
plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 3, figsize=(12.4, 3.7), dpi=150)

sc = ax[0].hist2d(deg, sens, bins=[np.arange(-.5, n+1.5), np.arange(-.5, n+1.5)],
                  cmap="magma", norm=matplotlib.colors.LogNorm())
xs = np.linspace(0.01, n, 200)
ax[0].plot(xs, np.sqrt(xs), color="#4dd6c1", lw=2.2, label=r"$s=\sqrt{\deg}$  (Huang)")
ax[0].set_xlabel("degree"); ax[0].set_ylabel("sensitivity")
ax[0].set_title("no function falls below the curve")
ax[0].legend(frameon=False, fontsize=8)
fig.colorbar(sc[3], ax=ax[0], label="functions")

w = np.zeros(n+1)
for k in range(n+1):
    w[k] = (coef**2)[:, popc == k].sum(axis=1).mean()
ax[1].bar(range(n+1), w, color="#d9a441")
ax[1].set_xlabel("Fourier level"); ax[1].set_ylabel("mean weight")
ax[1].set_title(f"average spectrum (sums to {w.sum():.4f})")

for nm, arr, c in (("s", sens, "#4dd6c1"), ("bs", bsv, "#d9a441"),
                   ("C", crt, "#ef5a5a"), ("D", dtv, "#e8e4d9")):
    cnt = np.bincount(arr, minlength=n+1)
    ax[2].plot(range(n+1), cnt, marker="o", ms=4, lw=1.8, color=c, label=nm)
ax[2].set_yscale("log"); ax[2].set_xlabel("value"); ax[2].set_ylabel("functions")
ax[2].set_title("complexity measures, exact counts"); ax[2].legend(frameon=False, fontsize=8)
for a_ in ax: a_.grid(alpha=.2)
fig.tight_layout(); fig.savefig("/mnt/user-data/outputs/census-landscape.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.0, 4.4), dpi=150)
im = ax.imshow(A, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_title(f"Huang's signing $A_{n}$  —  $A^2={n}I$", fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(im, ax=ax, fraction=.046, label="edge sign")
fig.tight_layout(); fig.savefig("/mnt/user-data/outputs/census-huang-matrix.png")
plt.close(fig)

print("\nplots written: census-landscape.png, census-huang-matrix.png")
print("="*66)
