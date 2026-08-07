# Boolean Sensitivity & Modular Arithmetic Research

A research thread exploring the complexity landscape of Boolean functions — sensitivity theory, Huang's 2019 Sensitivity Theorem, a residue/gap conjecture for cyclically invariant functions, and a detour into what modular arithmetic actually explains (and doesn't) about "magic" number patterns.

## Contents

| File | What it does |
|---|---|
| `code/census.py` | Exhaustively computes the complexity landscape for all 2^16 Boolean functions on 4 variables; verifies Huang's Sensitivity Theorem from scratch. |
| `code/profile-solver.py` | Exact solver over the *profile graph* (not the necklace graph) to find true sensitivity floors for cyclically invariant functions — cheap enough to reach sizes brute force can't. |
| `docs/two-families-output.pdf` | States and stress-tests a conjecture: for every n, the minimum sensitivity of a non-constant cyclically invariant Boolean function is attained by a **residue** family or a **gap** family — never neither. Includes falsifiable predictions. |
| `docs/p-vs-np-memo.md` | Research memo: not a proof of P ≠ NP, but a specification — derived from the three major barrier theorems (relativization, natural proofs, algebrization) — of properties any valid separating proof must have. |
| `docs/deep369-output.pdf` | Traces the real math under the "3-6-9" numerology claim down through repeating decimals, primitive roots, and Artin's conjecture (still open) to Dirichlet characters and the Riemann Hypothesis. |
| `docs/audit369-output.pdf` | A skeptical audit of the "3, 6, 9 — key to the universe" Tesla quote: confirms the arithmetic pattern is real, shows it's a base-10 artifact (proven: base 10 is the *unique* base producing exactly 3 special residues), and finds no primary source for the quote. |

## Status

Research-stage. `p-vs-np-memo.md` contains no proof and claims none — it's a spec for what a proof would need to look like. The residue/gap conjecture in `two-families-output.pdf` is falsifiable and open (see "What would break this" section): a single sensitivity-4 cyclically invariant function on 13 or 15 bits would kill it.

## Running the code

```bash
pip install numpy matplotlib
python3 code/census.py
python3 code/profile-solver.py
```
