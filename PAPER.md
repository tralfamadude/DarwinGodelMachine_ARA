---
title: "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents"
authors:
  - Jenny Zhang
  - Joel Lehman
  - Kenneth Stanley
  - Jeff Clune
year: 2025
venue: "ICLR 2026"
doi: "arXiv:2505.22954"
ara_version: "1.0"
domain: "Artificial Intelligence / Self-Improving Systems / Evolutionary Algorithms"
keywords:
  - self-improving AI
  - open-ended evolution
  - Gödel Machine
  - coding agents
  - LLM-guided evolution
  - SWE-bench
  - Polyglot benchmark
  - archive-based search
  - evolutionary algorithms
  - agent self-modification
claims_summary:
  - "DGM achieves 50.0% on SWE-bench Verified and 38.0% on Polyglot by open-ended evolutionary self-modification of its own coding agent code"
  - "Removing open-ended exploration drops SWE-bench performance by 27 percentage points (50.0% → 23.0%), establishing it as the primary driver of gains"
  - "Keep-all archive beats greedy selection by 10.3 pp on SWE-bench (50.0% vs 39.7%), demonstrating that diversity preservation is essential"
  - "DGM produces 51.3% functionally capable agents vs 32.5% for ablation variants"
  - "DGM generalizes to novel objectives (hallucination reduction) but surfaces objective hacking as a co-discovered failure mode"
abstract: "We present the Darwin Gödel Machine (DGM), a self-improving system that iteratively modifies its own code and empirically validates each change using coding benchmarks. Unlike the original Gödel Machine—which requires formal proofs of improvement that are computationally intractable—DGM replaces formal proofs with empirical evaluation on software engineering benchmarks. DGM maintains an archive of all valid agent variants discovered during search and uses performance-proportional parent selection with a novelty bonus to guide open-ended evolutionary exploration. Applied to coding tasks, DGM discovers substantial improvements to its own coding agent: achieving 50.0% on SWE-bench Verified and 38.0% on Polyglot. Ablation studies show that both self-improvement (LLM-guided code modification) and open-ended exploration (archive-based diversity preservation) are necessary; removing open-ended exploration causes the largest performance drop. DGM also demonstrates generalization to a hallucination-reduction objective, while surfacing objective hacking as a risk in automated self-improvement."
---

# Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents

## Overview

The Darwin Gödel Machine (DGM) is a self-improving AI system that automatically discovers improvements to its own coding agent code through open-ended evolutionary search guided by large language models. The system maintains an archive of all valid agent variants and uses performance-proportional parent selection with a novelty bonus (score-child-proportional selection) to explore the space of self-modifications without collapsing to local optima.

DGM replaces the formal-proof requirement of the original Gödel Machine (Schmidhuber, 2003) with empirical validation on coding benchmarks (SWE-bench Verified, Polyglot). Each generation, an LLM diagnoses failing benchmark tasks, proposes code modifications to the current coding agent, and the modified agent is evaluated on a 60-task subset; agents passing a score threshold proceed to full 200-task evaluation. All valid agents (those that compile and have basic functionality) are retained in the archive regardless of score, preserving diversity. Key discovered improvements include enhancing the editor tool with `str_replace` and line-range viewing, context summarization for long conversations, and multi-candidate generation.

## Layer Index

### Cognitive Layer (`/logic`)

| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight: why open-ended empirical self-improvement? |
| [claims.md](logic/claims.md) | 6 falsifiable claims (C01–C06) covering performance, ablations, diversity, and generalization |
| [concepts.md](logic/concepts.md) | 9 formal definitions: DGM, archive, parent selection, empirical validation, objective hacking, etc. |
| [experiments.md](logic/experiments.md) | 5 declarative verification plans (E01–E05): main evals, ablations, functionality, hallucination |
| [solution/architecture.md](logic/solution/architecture.md) | 9-component system graph: outer loop, archive, selector, workers, agent, meta-LLM, evaluator |
| [solution/algorithm.md](logic/solution/algorithm.md) | Mathematical formulation of parent selection + full outer-loop pseudocode + complexity |
| [solution/constraints.md](logic/solution/constraints.md) | Compute cost, benchmark dependency, Docker requirement, objective hacking risk |
| [solution/heuristics.md](logic/solution/heuristics.md) | 6 heuristics (H01–H06): partial eval, sigmoid scaling, novelty bonus, keep-all, Docker, cumulative patching |
| [related_work.md](logic/related_work.md) | Typed dependency graph (RW01–RW14) covering Gödel Machine, open-ended evolution, SWE-bench, ADAS, etc. |

### Physical Layer (`/src`)

| File | Description | Claims |
|------|-------------|--------|
| [execution/dgm_outer.py](src/execution/dgm_outer.py) | Outer evolutionary loop: archive management, generation loop, parallel workers | C01, C02, C04 |
| [execution/parent_selection.py](src/execution/parent_selection.py) | Score-child-proportional parent selection with sigmoid scaling and novelty bonus | C02, C04 |
| [configs/training.md](src/configs/training.md) | Evolution hyperparameters: generations, workers, selection method, eval thresholds | C01–C04 |
| [configs/model.md](src/configs/model.md) | LLM configurations: Claude 3.5 Sonnet (New) for self-modification, model variants per benchmark | C01 |
| [environment.md](src/environment.md) | Python 3.10, Anthropic/OpenAI SDK, Docker, SWE-bench, hardware requirements |  |

### Exploration Graph (`/trace`)

| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 12-node research DAG: central question → design decisions → ablation dead-ends → generalization |

### Evidence (`/evidence`)

| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 5 tables (incl. 1 derived) + 2 figures mapped to claims |
| [tables/table1_main_results.md](evidence/tables/table1_main_results.md) | Main results: DGM vs ablations on SWE-bench and Polyglot |
| [tables/table2_agent_functionality.md](evidence/tables/table2_agent_functionality.md) | % of generated agents with basic code-editing functionality |
| [tables/table3_foundation_models.md](evidence/tables/table3_foundation_models.md) | Foundation models used per experiment setting |
| [tables/appendix_e1_compute_costs.md](evidence/tables/appendix_e1_compute_costs.md) | Estimated compute costs per experimental configuration (Appendix E.1) |
| [figures/figure2_performance_curves.md](evidence/figures/figure2_performance_curves.md) | Performance over DGM generations on SWE-bench and Polyglot |
| [figures/figure8_hallucination_archive.md](evidence/figures/figure8_hallucination_archive.md) | Archive scores for hallucination-reduction case study |
