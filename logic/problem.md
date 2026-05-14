# Problem Specification

## Observations

### O1: Existing coding agents plateau without self-modification
- **Statement**: State-of-the-art coding agents built on fixed LLM APIs (e.g., Claude 3.5 Sonnet on SWE-bench) reach performance ceilings that do not improve through prompt engineering alone; benchmark leaders require substantial human engineering of agent scaffolding.
- **Evidence**: SWE-bench leaderboard (as of paper submission): top systems (e.g., OpenHands + CodeAct v2.1) require careful manual design; the initial DGM agent (before self-improvement) represents a human-engineered baseline.
- **Implication**: Performance gains require structural changes to the agent's code, not just better prompts or larger models.

### O2: The original Gödel Machine is practically intractable
- **Statement**: Schmidhuber's (2003) Gödel Machine self-rewrites only when it can formally prove the rewrite improves expected future reward. Such proofs are computationally intractable for real-world programs of non-trivial size.
- **Evidence**: No practical implementation of the original Gödel Machine exists for real-world agent code; the formal proof requirement is cited as the key barrier (§1, §2 of the paper).
- **Implication**: An empirical substitute for formal proofs is necessary to make self-improvement practical.

### O3: Open-ended evolution preserves diversity but has lacked LLM-scale variation operators
- **Statement**: Open-ended evolutionary algorithms (e.g., MAP-Elites, novelty search) maintain diverse solution archives to avoid premature convergence, but have traditionally relied on hand-designed mutation operators that do not generalize to complex program spaces.
- **Evidence**: Stanley & Lehman (2015), Lehman et al. (2022); prior evolutionary coding systems required domain-specific operators (§2 related work).
- **Implication**: LLMs can serve as general-purpose variation operators for program-space search, enabling open-ended evolution of agent code without hand engineering.

### O4: LLMs can diagnose failures and propose targeted code modifications
- **Statement**: Large language models (LLMs such as Claude 3.5 Sonnet, o1) can analyze execution logs, identify failure modes, and propose code-level modifications to agent scaffolding.
- **Evidence**: DGM's self-improvement step (§3, Appendix A.1, A.2) demonstrates LLM-guided diagnosis and modification at scale across 80 generations; repo: `self_improve_step.py`, `prompts/self_improvement_prompt.py`.
- **Implication**: LLMs enable automatic generation of meaningful code variations without human intervention.

## Gaps

### G1: No scalable system for automatic, continuous coding-agent self-improvement
- **Statement**: There is no prior system that (a) automatically modifies its own agent code, (b) validates modifications empirically at scale, and (c) maintains an open-ended archive of discovered improvements for continued exploration.
- **Caused by**: O2 (intractable formal proofs), O3 (lack of general variation operators)
- **Existing attempts**: ADAS (Automated Design of Agentic Systems) proposes agent modifications but uses a fixed search procedure without open-ended exploration or archive diversity.
- **Why they fail**: Greedy or single-trajectory search collapses to local optima; without diversity preservation, improvements requiring multi-step sequences through temporarily worse states are not discovered.

### G2: Formal proof requirement prevents practical self-improvement
- **Statement**: The original Gödel Machine's requirement for a formal proof of improvement is computationally intractable for realistic agent programs, blocking adoption of provably self-improving systems.
- **Caused by**: O2
- **Existing attempts**: Theoretical work on Gödel Machines (Schmidhuber, 2003, 2007) remains unimplemented in practice.
- **Why they fail**: Program verification and theorem proving for real-world software is undecidable in the general case; tractable approximations sacrifice the soundness guarantee.

### G3: Self-improvement systems risk objective hacking
- **Statement**: Automated self-improvement systems that optimize a measurable proxy objective may discover solutions that maximize the proxy without solving the underlying task (Goodhart's Law / reward hacking).
- **Caused by**: O4 (LLMs are capable of creative optimization)
- **Existing attempts**: Reward hacking literature (Skalse et al., 2022) characterizes this problem for RL systems; it has not been systematically studied for LLM-based self-modifying agents.
- **Why they fail**: Current benchmarks do not distinguish between genuine capability improvement and benchmark gaming without human oversight.

## Key Insight

- **Insight**: Replacing formal proofs with empirical evaluation on coding benchmarks, and combining LLM-guided code modification with open-ended archive-based diversity preservation, yields a practically tractable self-improving agent system. The LLM acts as both variation operator (proposing code changes) and diagnostic oracle (analyzing failures), while the benchmark acts as the fitness function.
- **Derived from**: O1, O2, O3, O4
- **Enables**: An evolutionary outer loop that continuously discovers and accumulates coding-agent improvements, avoiding local optima through archive diversity and scaling to real-world software engineering benchmarks.

## Assumptions

- A1: Coding benchmarks (SWE-bench Verified, Polyglot) provide sufficient signal for evaluating agent quality; performance on 60-task subsets is predictive of full 200-task evaluation.
- A2: LLMs can propose meaningful and implementable code modifications given failure logs and the current agent codebase.
- A3: Cumulative patching (applying all ancestor git patches) correctly reconstructs any agent variant in the lineage.
- A4: Docker-isolated evaluation prevents cross-contamination between agent variants.
- A5: The initial coding agent has sufficient baseline functionality to serve as a starting point for productive self-improvement.
- A6: Agent functionality improvements on one LLM backbone (Claude 3.5 Sonnet) can generalize to a different backbone (o3-mini) without re-training.
