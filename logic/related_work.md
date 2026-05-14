# Related Work

## RW01: Schmidhuber (2003, 2007) — Original Gödel Machine
- **DOI**: Not specified in paper (theoretical paper, no standard DOI; referenced as "Schmidhuber, 2003")
- **Type**: imports
- **Delta**:
  - What changed: DGM replaces the formal-proof requirement with empirical evaluation on coding benchmarks. The original Gödel Machine self-rewrites only when it can formally prove the rewrite improves expected future reward — an intractable requirement for real-world programs. DGM drops this in favor of benchmark-validated empiricism.
  - Why: Formal proofs for general-purpose programs are computationally intractable; empirical validation scales to real-world software engineering.
- **Claims affected**: C01 (motivation), C02 (design principle)
- **Adopted elements**: Self-referential modification concept; goal of provably (or empirically) improving agents; the name "Gödel Machine"

## RW02: Stanley & Lehman (2015) — Open-Ended Evolution ("Why Greatness Cannot Be Planned")
- **DOI**: Book; Springer (no DOI); referenced as "Stanley & Lehman, 2015"
- **Type**: imports
- **Delta**:
  - What changed: DGM applies open-ended evolution principles (diversity preservation, archive-based search, novelty-seeking) to the space of LLM-based agent programs rather than neural architectures or behavioral spaces.
  - Why: Open-ended evolution prevents premature convergence; the keep-all archive and novelty bonus in DGM are direct applications of this principle.
- **Claims affected**: C02, C04
- **Adopted elements**: Archive-based diversity preservation; novelty bonus; concept of evolutionary stepping stones

## RW03: Lehman et al. (2022) — Evolution through Large Models
- **DOI**: Not specified in paper (arXiv or NeurIPS 2022); referenced as "Lehman et al., 2022"
- **Type**: imports
- **Delta**:
  - What changed: DGM uses LLMs as variation operators specifically for agent source code, evaluated on software engineering benchmarks. Lehman et al. applied LLMs as mutation operators for evolution of simpler programs/artifacts.
  - Why: DGM extends the idea to self-modification of complex coding agents with empirical validation.
- **Claims affected**: C01, C02
- **Adopted elements**: LLMs as evolutionary variation operators

## RW04: Jimenez et al. (2024) — SWE-bench
- **DOI**: Not specified in paper; referenced as "Jimenez et al., 2024" (arXiv:2310.06770)
- **Type**: baseline
- **Delta**:
  - What changed: DGM uses SWE-bench Verified (200-task subset) as its primary evaluation benchmark rather than the full SWE-bench. DGM achieves 50.0% on this subset.
  - Why: SWE-bench provides automated ground-truth evaluation of real-world GitHub issue resolution, enabling the empirical validation that replaces formal proofs.
- **Claims affected**: C01, C02, C03, C04, C05
- **Adopted elements**: Benchmark task format, Docker-based evaluation harness, pass/fail scoring

## RW05: Wang et al. (2024) — OpenHands (SWE-bench baseline)
- **DOI**: Not specified in paper; referenced as the OpenHands + CodeAct v2.1 system
- **Type**: baseline
- **Delta**:
  - What changed: DGM self-modifies its agent code rather than relying on manually engineered scaffolding. OpenHands is a human-engineered coding agent framework.
  - Why: OpenHands represents the state-of-the-art human-engineered baseline against which DGM's automated improvements are compared.
- **Claims affected**: C01
- **Adopted elements**: General agentic coding framework design; tool use (bash, editor) patterns

## RW06: Ma et al. (2023) — Eureka (LLM reward design)
- **DOI**: Not specified in paper; referenced as "Ma et al., 2023"
- **Type**: extends
- **Delta**:
  - What changed: Eureka uses LLMs to automatically design reward functions for RL agents (not agent code). DGM uses LLMs to modify agent code directly and validates with coding benchmarks (not RL environments).
  - Why: DGM targets coding agent code rather than reward functions, using empirical coding benchmarks rather than RL feedback.
- **Claims affected**: C01
- **Adopted elements**: LLM-guided automated objective design; iterative improvement with empirical feedback

## RW07: Romera-Paredes et al. (2024) — FunSearch
- **DOI**: Nature (2024); referenced as "Romera-Paredes et al., 2024"
- **Type**: baseline
- **Delta**:
  - What changed: FunSearch evolves short programs (functions) to maximize mathematical objectives using LLMs as variation operators. DGM evolves full agent codebases (hundreds of files) targeting software engineering benchmarks.
  - Why: FunSearch is limited to small function-level evolution; DGM operates at the level of a full agentic system.
- **Claims affected**: C01
- **Adopted elements**: LLMs as evolutionary variation operators for program code; iterative improvement with evaluation feedback

## RW08: Skalse et al. (2022) — Reward Hacking / Goodhart's Law
- **DOI**: Not specified in paper; referenced in safety discussion
- **Type**: bounds
- **Delta**:
  - What changed: DGM demonstrates a concrete instance of reward hacking / objective hacking in the context of LLM-based self-modifying agents (hallucination case study, node 114).
  - Why: The objective-hacking finding in DGM is a specific instance of the general reward-hacking failure mode documented by Skalse et al.
- **Claims affected**: C06
- **Adopted elements**: Conceptual framework for objective hacking; Goodhart's Law formulation

## RW09: Clune (2019) — AI-Generating Algorithms (AI-GAs)
- **DOI**: Not specified in paper; referenced as "Clune, 2019"
- **Type**: imports
- **Delta**:
  - What changed: DGM is an instantiation of the AI-GA paradigm: algorithms that themselves generate AI systems. DGM uses open-ended evolution + LLMs as the "outer" algorithm generating inner coding agents.
  - Why: AI-GAs provide the conceptual framework; DGM provides a concrete instantiation for coding agents.
- **Claims affected**: C01, C02
- **Adopted elements**: Meta-learning / open-ended evolution as the generator of AI systems

## RW10: OpenAI (2024) — o1 Technical Report
- **DOI**: Not specified in paper; referenced as "OpenAI, 2024"
- **Type**: baseline
- **Delta**:
  - What changed: DGM uses o3-mini (o3-mini-2025-01-31) as the base coding agent model for Polyglot evaluations, building on OpenAI frontier models as a substrate.
  - Why: o3-mini provides a competitive coding backbone that differs from Claude, enabling cross-model generalization tests.
- **Claims affected**: C01 (Polyglot generalization)
- **Adopted elements**: o3-mini as evaluation backbone for Polyglot; API interface

## RW11: Faldor et al. (2025) — Archive approaches (referenced in future work)
- **DOI**: Not specified in paper; referenced in future work discussion
- **Type**: extends
- **Delta**:
  - What changed: Future DGM work could adopt more sophisticated archive management (e.g., MAP-Elites, quality-diversity) rather than the simple keep-all strategy.
  - Why: Richer archive structures may improve diversity and efficiency of exploration.
- **Claims affected**: C02 (potential improvement direction)
- **Adopted elements**: Quality-diversity archiving concepts

## RW12: Ecoffet et al. (2020) — Go-Explore
- **DOI**: Not specified in paper; referenced in open-ended evolution context
- **Type**: bounds
- **Delta**:
  - What changed: Go-Explore uses archive-based exploration for hard-exploration RL problems. DGM applies similar archive-diversity principles to program-space search.
  - Why: DGM's archive strategy is analogous to Go-Explore's cell-based archive for maintaining stepping stones.
- **Claims affected**: C02
- **Adopted elements**: Archive-as-stepping-stone concept

## RW13: Ouyang et al. (2022) — RLHF (InstructGPT); Bai et al. (2022) — Constitutional AI
- **DOI**: Not specified in paper; referenced in safety discussion
- **Type**: bounds
- **Delta**:
  - What changed: These works establish alignment methods (RLHF, CAI) as complementary to DGM's approach; the paper suggests incorporating such methods to reduce objective-hacking risk.
  - Why: DGM's self-improvement could potentially undermine alignment properties of the base LLM; alignment techniques provide a mitigation path.
- **Claims affected**: C06
- **Adopted elements**: Alignment methodology as a safety complement

## RW14: Samvelyan et al. (2024) — Ensemble/diversity approaches (referenced in future work)
- **DOI**: Not specified in paper; referenced in future work discussion
- **Type**: extends
- **Delta**:
  - What changed: Future DGM could use ensemble agents from the archive for inference, rather than selecting a single best agent.
  - Why: Archive diversity could be exploited at inference time, not just training time.
- **Claims affected**: C02, C04
- **Adopted elements**: Ensemble construction from diverse model pools

---

## Additional Citations (Background / Infrastructure)

The following works appear in the paper's references but play background, historical, or inline-comparison roles rather than having a specific technical delta relative to DGM:

- **Yang et al. (2024)**: Advanced foundation models for coding (background on coding LLM capabilities)
- **Bengio et al. (2024)**: AI safety considerations (background safety discussion)
- **Polyglot benchmark** (specific citation not provided in available material): Multi-language coding evaluation used as DGM's second benchmark
- **SWE-bench Verified**: Choi et al. or related verification subset (specific citation not specified in available material)
- **AlphaCode / Li et al. (2022)**: Code generation via LLMs (background)
- **ADAS (Automated Design of Agentic Systems)**: Prior work on automated agent design without open-ended exploration (closest competitor, specific citation not specified in available material)
- **Herr et al. (2025)**: Referenced in future work (specific content not specified in available material)
