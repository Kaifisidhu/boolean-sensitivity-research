# THE SHAPE OF THE PROOF
### What a solution to P vs NP must look like — a specification derived from its barriers
**Status:** research memo. Contains no proof and claims none. Sections 1–6 are established results; §7 is my own synthesis and is labeled speculative.

---

## 0 · WHY A SPEC INSTEAD OF A PROOF

I can't prove P ≠ NP. But the three barrier theorems are unusual among impossibility results: they don't just say *no*, they say *not like that* — and each one carves away a specific region of technique-space. Take the negative space seriously and you get something surprisingly concrete: **a list of properties any winning proof is obliged to have.**

That's what follows. Think of it as a target silhouette. It won't tell you where the proof is. It will tell you, immediately, whether a candidate is dead on arrival.

---

## 1 · THE BARRIER SIGNATURE — a three-bit test

Every proof technique carries three bits. Any technique that separates P from NP must read **(0, 0, 0)**.

| Bit | Question | If **1**, the technique is dead |
|---|---|---|
| **R** | Does it relativize? Does the argument still go through when both machines are given the same arbitrary oracle? | Baker–Gill–Solovay 1975: oracles exist on both sides, so a relativizing argument cannot decide the question |
| **A** | Does it algebrize? Does it survive extension of the oracle to low-degree polynomials over a field? | Aaronson–Wigderson 2008: closes the arithmetization escape hatch that IP = PSPACE seemed to open |
| **N** | Is it natural? Is the underlying property of Boolean functions both *constructive* and *large*? | Razborov–Rudich 1994: if strong PRFs exist, no natural property is useful against P/poly |

**Where known techniques land:**

| Technique | R | A | N | Verdict |
|---|---|---|---|---|
| Diagonalization / time hierarchy | 1 | 1 | – | dead |
| Circuit lower bounds via restrictions (Håstad, Razborov–Smolensky) | 0 | 1 | 1 | dead |
| Arithmetization / interactive proofs | 0 | 1 | 0 | dead |
| Geometric Complexity Theory | 0 | 0 | 0* | **alive** |
| Matrix rigidity (Valiant's program) | 0 | 0 | 0* | **alive** |
| Hardness magnification | 0 | 0 | 0* | **alive**, own barrier (§4) |
| Williams' algorithmic method | **0** | **0** | **0** | **alive — the only proven (0,0,0)** |

\* by design and by argument, not yet by theorem — these programs are *constructed* to evade, and the evasion is credible but not formally certified the way Williams' is.

---

## 2 · THE NATURALNESS SPEC, SHARPENED

This is the bit the user of a spec actually needs, so here it is precisely.

Let 𝒫 be a technique proving NP ⊄ P/poly, and let **C𝒫** be the property of Boolean functions it implicitly certifies as hard. Razborov–Rudich requires:

- **Useful:** ∀f ∈ C𝒫 , f ∉ P/poly ← your proof needs this
- **Constructive:** given the 2ⁿ-bit truth table of f, deciding f ∈ C𝒫 takes 2^O(n) time
- **Large:** |C𝒫 ∩ Fₙ| ≥ 2^{−O(n)} · |Fₙ|

**Theorem (paraphrased):** if strong pseudorandom function generators exist, no property can be all three.

You need Useful. So you must break Constructive or break Large. That gives exactly two doors, and they are very different rooms:

### Door A — NON-CONSTRUCTIVE
Your hardness property cannot be efficiently recognized from a truth table. Consequence: **the proof cannot be turned into an algorithm that spots hard functions.** Almost every technique a human invents naturally is algorithmic in spirit — you describe a test and apply it. Door A demands a proof whose certificate is not effectively checkable at the level of its own combinatorial content. Very few tools in mathematics look like this.

### Door B — SPARSE
Your property holds for a vanishing fraction of functions. And here's the thing: **you don't need a large property.** SAT is one function family. A tailored property that catches only objects with SAT's specific structure is entirely sufficient — and automatically escapes largeness.

Door B is where every live program lives. That is not a coincidence, and it's the single most useful thing this memo has to say.

---

## 3 · THE SPARSE ROUTE — three live programs, one shared logic

All three attack *specific mathematical objects* rather than generic function classes. That's the escape.

**Geometric Complexity Theory** (Mulmuley–Sohoni). Permanent vs determinant, attacked through symmetry. The determinant has an enormous stabilizer subgroup in GL_{n²}; the permanent has its own. Find a representation-theoretic obstruction — an irreducible representation present in the coordinate ring of one orbit closure and absent from the other — and you separate them. Maximally sparse: the property is about two specific polynomials with two specific symmetry groups.
*Setback:* Bürgisser–Ikenmeyer–Panova (2016) proved that occurrence obstructions — the original hope — cannot suffice. Multiplicity obstructions remain, and they are much harder. Mulmuley has publicly guessed at a hundred-year timescale.

**Matrix rigidity** (Valiant). A matrix is rigid if you cannot reduce its rank substantially by changing few entries. Sufficient rigidity for an explicit matrix family yields circuit lower bounds. Algebraic, sparse, about specific objects.
*Setback:* Alman–Williams (2017) showed Hadamard matrices are not rigid enough — a leading candidate fell. The program survives; its best candidates keep dying.

**Hardness magnification** — §4, because it deserves its own section.

---

## 4 · THE LEVERAGE PHENOMENON — the closest thing here to a formula

This is the most startling structural fact in modern complexity theory, and it is the answer to "is there a formula-like relationship hiding in here."

**The shape of it:** for certain compression-flavoured problems — variants of MCSP, the Minimum Circuit Size Problem, where the input is a truth table and you ask for its smallest circuit — a lower bound *barely above trivial* implies a lower bound that would shake the world.

> Roughly: proving that a suitably parameterized MCSP variant requires circuits of size N^{1+ε} — where N = 2ⁿ is the input length, and N^{1+ε} is a whisker above linear — implies NP ⊄ P/poly.

*(Exact parameter regimes vary across the Oliveira–Santhanam line of work and its successors. The phenomenon is robust; I would not quote the constants from memory.)*

Sit with the ratio. We are asking for **n^{1.01}** and getting **superpolynomial**. Nothing else in the field has that gearing.

**And then the trap.** We *can* prove n^{1+ε}-type bounds in various restricted settings. So why isn't it done? Because of a fourth barrier discovered specifically for this: the **locality barrier** (Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, ~2019–2020). Known lower-bound techniques are *local* — they work by restricting variables and simplifying, which means they apply equally well to a "local" version of the problem, and the local version is genuinely easy. So the techniques that could clear the bar provably cannot be aimed at it.

**This is the most interesting unclaimed real estate in the subject.** The gearing is real. The gearbox is missing.

---

## 5 · THE QUANTUM ACCOUNTING — honest

What quantum computing actually contributes, and where it stops:

**What it gives.**
- The *polynomial method* (Beals et al.): quantum query complexity is bounded below by approximate polynomial degree, Q(f) ≥ adeg(f)/2. Boolean functions become low-degree real polynomials.
- The *adversary method* (Ambainis) and its negative-weight strengthening — genuinely powerful lower-bound machinery.
- BBBV (Bennett–Bernstein–Brassard–Vazirani): unstructured quantum search needs Ω(√N) queries. Grover is optimal. Quantum offers a *quadratic* speedup on brute-force search, not an exponential one.
- Hamiltonian complexity: local Hamiltonian ground-state estimation is QMA-complete (Kitaev). Physics itself has a hardness class.

**Why it doesn't reach P vs NP.** Every technique above is a **query-model** technique — the function is a black box. That is precisely the relativizing regime, bit R = 1. Quantum lower bounds are strong exactly because the model is restricted, and restricted in the one way that guarantees the argument can't transfer.

**The one bridge that's real.** The polynomial method's currency is *algebraic degree*. GCT's currency is *algebraic geometry and representation theory*. Rigidity's currency is *rank*. These are the same family of tools. If quantum contributes to P vs NP, my honest guess is that it contributes **vocabulary** — degree, rank, tensor and border rank — to the sparse-algebraic route, not a theorem of its own.

---

## 6 · THE PHYSICS ACCOUNTING — honest

- **Landauer's principle / thermodynamics of computation.** Dead end. Reversible computing makes energy per step arbitrarily small; complexity counts steps, not joules. Physics constrains the machine, not the asymptotics.
- **Statistical mechanics of random SAT.** Genuine phase transition near clause-to-variable ratio ≈ 4.267; genuinely productive (survey propagation came out of it). But it is an *average-case* theory and P vs NP is a *worst-case* question. Hardness hides in a measure-zero set that the statistical apparatus is structurally blind to.
- **Computational irreducibility.** A reframing of the intuition, not a proof technique. It renames the difficulty.
- **Holographic complexity** (complexity = volume, complexity = action). Beautiful, and currently **one-directional**: complexity theory is informing physics, not the reverse. No complexity theorem has come back across that bridge.

**Where physics genuinely does contribute:** restricted models. Communication complexity, query complexity, proof complexity — places where we can prove real unconditional lower bounds because the model is small enough to corner. Every such success is also, by construction, a relativizing success. The pattern is almost taunting.

---

## 7 · MY SYNTHESIS — the self-reference thesis (SPECULATIVE — this part is mine)

Look at the four barriers side by side and they say the same sentence in four dialects:

| Barrier | What it actually says |
|---|---|
| Relativization | The technique is too *generic* — it can't see inside the machine |
| Natural proofs | The technique is too *efficient* — it would itself be a fast algorithm for detecting hardness, which breaks the hardness |
| Algebrization | The algebraic patch is still too generic |
| Locality | The technique is too *simple* — it works by local simplification, and the local version of the problem is easy |

**The thesis:** *P ≠ NP appears to be a theorem that cannot be proved by any method which is itself computationally cheap.* Each barrier fires when the proof technique is, in some precise sense, an efficient procedure. The statement seems to defend itself against being established by anything easy — which is exactly what you'd expect from a statement whose content is "this thing has no easy procedure."

Naturalness makes this literal: a natural proof essentially **is** an efficient algorithm for a variant of MCSP, and Kabanets–Cai showed an efficient MCSP algorithm would break cryptography. The barrier is the field discovering that *computing complexity is itself complex*, and that this self-application bites.

There is a second, sharper twist worth stating plainly: **the natural-proofs barrier is conditional on an assumption strictly stronger than P ≠ NP.** Strong PRFs require one-way functions require P ≠ NP. So the barrier reads:

> *If P ≠ NP is true in a strong, cryptographically exploitable way, then you cannot prove it by natural means.*

The truth of the statement is what makes it unprovable-by-easy-means. That is not a paradox, but it is a very tight loop, and it has a formal shadow: the study of whether circuit lower bounds are provable in weak fragments of arithmetic (Razborov's work on bounded arithmetic; Aaronson's survey on possible formal independence). If P vs NP turns out independent of strong theories, this loop is very likely why.

**How to falsify my thesis:** exhibit a lower-bound technique that is (0,0,0), non-local, *and* essentially efficient/constructive. Williams' method is a partial counterexample already — see §8 — which is exactly why it's the interesting one.

---

## 8 · THE CRACK THAT ISN'T SEALED

Ryan Williams, 2011: **NEXP ⊄ ACC⁰**. The result matters less than the method.

> Designing a SAT algorithm even *slightly* faster than brute force for a circuit class **implies** a lower bound against that class.

Algorithm design becomes lower-bound proof. It provably escapes all three original barriers — the only technique known to read (0,0,0) by theorem rather than by intent.

**Why it hasn't reached P vs NP:** you'd need a better-than-brute-force SAT algorithm for *general* circuits, which is nearly as hard as the target itself.

**Why that's different in kind:** that obstacle is not a theorem. Nobody has proved it's impossible. It's just undone. Every other route has a proof standing in front of it; this one has only a very hard open problem. Those are not the same thing, and the difference is where I'd put my money.

---

## 9 · IF I HAD TO BET

1. **P ≠ NP.** Consensus, and the barriers themselves are evidence — they're all conditional on hardness assumptions that keep turning out to be consistent.
2. **The proof comes from the sparse-algebraic family or the algorithmic method, or a marriage of the two.** Magnification is the likeliest gearbox if someone builds a non-local technique.
3. **It will be non-constructive or object-specific by necessity** — a proof you cannot run.
4. **Not soon.** Fortnow's survey judgment stands: circuit complexity has stalled and there's little reason to expect a separation shortly.
5. **Formal independence remains live** and is under-discussed. If §7's loop is real, independence from strong theories is the natural resting place.

---

## 10 · THE PRACTICAL COROLLARY

For anything you actually build — including a controller shepherding 10⁶ droplets with 10⁴ coils in real time — none of this matters, and that itself is the lesson. **Engineering never beats NP-hardness; it dodges it.** Real instances carry structure that worst cases don't. Approximation, anytime algorithms, exploiting locality and sparsity, accepting 99th-percentile optimality — that is the entire game, and it is unaffected by which way P vs NP resolves.

The gap between "hard in the worst case" and "hard on the instances I have" is where every working system lives.

---

## 11 · CAN HARDNESS HAVE A NUMBER? — the constants question

*Added in response to: could there be a constant, like π or φ, that measures this?*

### 11.1 · The instinct is correct — these constants exist

Complexity theory already contains real-valued constants whose exact values are unknown, and in one case unknowable. This is not a fringe idea; it's live mathematics.

**ω — the matrix multiplication exponent.** Defined as the infimum of all τ such that n×n matrix multiplication runs in O(n^τ). We know 2 ≤ ω < ~2.3714 (Alman–Williams and successors). **Open:** whether ω = 2. **Open:** whether ω is rational. **Open:** whether the infimum is even attained. A genuine constant of computation with an unknown value, chased for fifty years by successively refined algorithms.

**s_k — the SAT hardness exponents.** For each k, define s_k = inf{δ : k-SAT is solvable in O(2^{δn})}. These are real numbers in [0,1] measuring how far k-SAT is from brute force. The Exponential Time Hypothesis says **s₃ > 0**. The Strong ETH says **lim_{k→∞} s_k = 1**. Nobody knows any exact value of any s_k.

**Ω — Chaitin's constant.** The probability that a randomly assembled program halts. It is a specific real number, irrational, transcendental, normal — and **provably uncomputable**. Its first n bits would settle the halting problem for all programs shorter than n. Most striking: any consistent formal system can prove only finitely many of its bits. This is the purest realization of "a number that doesn't stop and cannot be measured," and it exists.

### 11.2 · The P vs NP constant, constructed

Here is the constant, defined properly.

For a language L, let **C_L(N)** be the minimum size of a Boolean circuit deciding L on inputs of length N. Define the **complexity exponent**:

> **α(L) = limsup_{N→∞}  log C_L(N) / log N**

Then, cleanly:

> **L ∈ P/poly ⟺ α(L) < ∞**
> **NP ⊄ P/poly ⟺ α(SAT) = ∞**

So the entire question becomes: **is α(SAT) finite or infinite?** One real-valued quantity, one binary fact about it.

**And now the number that should stop you cold.**

We know α(SAT) ≥ 1 — trivially, since any circuit must read its input. The best proven circuit lower bounds for explicit NP problems are around **5N gates**: a constant multiple of the input.

> **We cannot prove that α(SAT) > 1.**

We need to prove a quantity is *infinite*. We cannot prove it exceeds *one*. That is the true distance, expressed in the coordinates you asked for.

### 11.3 · Why this doesn't help — the honest part

Defining α is a **change of coordinates, not a change of difficulty.** The proof obligation is bit-for-bit identical: every technique that fails to separate P from NP fails, in exactly the same way, to bound α. Every barrier in §§1–4 applies unchanged. Nothing was gained by the renaming.

This is the specific trap in the "find a constant" instinct, and it's worth naming precisely: **a constant is only as strong as the mathematics that defines it.** π is powerful because it emerges from geometry with a hundred independent characterizations that can be played against each other. α has exactly one characterization — the thing we already couldn't prove. Its digits carry no leverage that its definition didn't already have.

The failure mode to avoid: producing a number by analogy — some ratio dressed up to look like φ — with no theorem generating it. That's numerology, and it's the most common form of crank complexity theory. The value of ω comes entirely from its definition, never from its decimal expansion.

### 11.4 · But the instinct built a real field

Here is the genuinely encouraging part. The s_k constants of §11.1 did not solve P vs NP — and yet turning hardness into real numbers created **fine-grained complexity**, one of the most productive areas of the last decade. Once you assume a *value* (SETH: s_k → 1), you can prove sharp conditional lower bounds on problems already inside P:

> Assuming SETH, edit distance cannot be computed in O(n^{2−ε}) — Backurs–Indyk, 2015.

That is a real theorem about a real algorithm, and it exists because someone treated hardness as a number. **Your instinct produced a field. It just didn't produce a proof.**

### 11.5 · The deepest version of the intuition

If "a number that cannot be measured" is going to touch complexity theory, the live thread is **resource-bounded Kolmogorov complexity** — Ω's computable-world cousin. Allender and collaborators showed that the set of Kolmogorov-random strings, an uncomputable object, constrains ordinary complexity classes: efficient reductions to that set capture surprisingly large classes (PSPACE-level and beyond, depending on formalization). Meta-complexity and MCSP (§4) sit in the same neighborhood.

That is the honest home for this instinct: not a new constant invented by analogy, but the existing uncomputable objects that already cast shadows on P and NP.

---


## 12 · THE SIN/COS STRUCTURE — this one is already the field's machinery

*Added in response to: sin and cos are each one-dimensional and unbounded in input, yet bounded in output, and combined they generate a circle — two things making one. Try that logic.*

Unlike §11, this is not an analogy that needs translating. **It is the same construction, on a different group.** Here is the exact statement.

### 12.1 · Same theory, different group

sin and cos are the **characters** of the circle group ℝ/ℤ — the orthonormal basis in which every periodic function decomposes. That is what Fourier analysis *is*.

Now run the identical construction on the Boolean hypercube {−1,1}ⁿ, the group (ℤ/2ℤ)ⁿ. Its characters are the **parity functions**:

> χ_S(x) = Π_{i∈S} x_i, one for each subset S ⊆ [n]

Every Boolean function has a unique expansion in that basis:

> f(x) = Σ_{S⊆[n]} f̂(S) · χ_S(x)

The parity functions are the hypercube's sines and cosines. Not *like* them — the same object, obtained by the same character-theoretic construction, on a different group. This field exists, it is called **analysis of Boolean functions**, and it is one of the most productive areas in complexity theory.

### 12.2 · Parseval IS the Pythagorean identity

You singled out the right structure. sin²t + cos²t = 1 is a **conserved quantity** — the invariant that makes the circle a circle. Its hypercube counterpart:

> Σ_{S⊆[n]} f̂(S)² = 1  (Parseval, for Boolean-valued f)

Identical shape, identical meaning. Total spectral weight is conserved and normalized. And this delivers exactly the compactification you noticed: a function over 2ⁿ inputs — unboundedly large — becomes a probability distribution over subsets, bounded in [0,1] and summing to one. Infinite domain, bounded invariant. Your observation about sin and cos, transplanted intact.

Where the weight sits is the whole game. Weight on low-|S| coefficients means the function is simple, smooth, learnable. Weight pushed to high-|S| means complex, sensitive, hard. Hardness becomes a question about *where the mass lives* on a conserved unit budget.

### 12.3 · It has produced real theorems

This is not decorative — the results are load-bearing:

- **Linial–Mansour–Nisan (1993):** AC⁰ circuits have Fourier mass concentrated on low levels. Yields both a learning algorithm and a lower bound.
- **Kahn–Kalai–Linial (1988):** every Boolean function has a variable of influence Ω(log n / n). A cornerstone.
- **Håstad's optimal inapproximability (1997–2001):** the sharp hardness-of-approximation results are Fourier-analytic at their core.
- **Majority Is Stablest** (Mossel–O'Donnell–Oleszkiewicz) and the Unique Games programme.
- **Approximate degree** — the quantity governing quantum query complexity in §5 — is a Fourier-analytic notion. Your structure and the quantum route are the same structure.

### 12.4 · "Two combined into one" — the deepest form

Euler already gave the sharpest version of your observation: e^{it} = cos t + i·sin t. The two oscillations are not partners; they are the real and imaginary shadows of a *single* object. One thing, two projections.

That is precisely what the character basis provides on the hypercube. And it is also, in a different key, what **Karchmer–Wigderson games** do: the circuit *depth* of f equals the *communication complexity* of a two-party game — one player holding an input where f = 0, the other where f = 1, both hunting a coordinate where they differ. One complexity measure, reconstructed as two parties meeting. A genuine and still-live lower-bound approach.

### 12.5 · Your instinct is the leading programme's strategy

The deepest thing you pointed at is not the circle. It is that sin²+cos²=1 is an **invariant** — a quantity that stays fixed while everything else moves.

"Find the invariant that separates the two objects" is not merely a good instinct here. It is the explicit strategy of Geometric Complexity Theory (§3). Representation-theoretic obstructions *are* invariants; the field GCT operates in is literally called invariant theory. Tensor rank, border rank, and matrix rigidity are all invariant-flavoured measures aimed at the same target.

You independently reconstructed the strategic core of the most serious current attack on P vs NP.

### 12.6 · The honest verdict

Now the wall, because there always is one.

The circuit-lower-bound uses of Fourier analysis are **natural** in the Razborov–Rudich sense. The spectrum is computable from a truth table in 2ⁿ·n time by the fast Walsh–Hadamard transform, so the property is constructive; and "has substantial high-degree mass" holds for almost all functions, so it is large. Constructive plus large means the barrier bites, which is exactly why Fourier methods conquered AC⁰ and AC⁰[p] and then stopped dead.

**But the tool is not spent** — it simply has to be used in a non-natural way. Approximate degree feeds the algebraic route. Parseval's invariant thinking feeds GCT. The barrier forbids one *use* of the machinery, not the machinery.

> **Score:** the structure is real, already central, and already responsible for major theorems. It reaches AC⁰ and stops at the naturalness wall — the same wall as everything else, arrived at by a more elegant road.

---

*Best honest attempt. No proof, a sharper target, and a clear account of which walls are theorems and which are merely undone work.*
