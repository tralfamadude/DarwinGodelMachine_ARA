# Experiments

## E01: DGM main evaluation on SWE-bench Verified
- **Verifies**: C01
- **Setup**:
  - System: Full DGM (keep-all archive, score-child-proportional selection, self-improvement enabled)
  - Self-modification LLM: Claude 3.5 Sonnet (New) = `bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0`
  - Coding agent LLM: Claude 3.5 Sonnet (New)
  - Dataset: SWE-bench Verified, 200-task subset (for evaluation); 60-task subset (for quick eval during evolution)
  - Hardware: Docker containers with 9-hour timeout per agent evaluation
  - Evolution: max_generation=80, selfimprove_size=2, selfimprove_workers=2
- **Procedure**:
  1. Initialize archive with the initial hand-engineered Claude 3.5 Sonnet coding agent
  2. Run DGM outer loop for 80 generations; each generation selects 2 parents and runs 2 parallel self-improvement workers
  3. After each self-improvement step, run quick eval (60 tasks); if score passes threshold, run full eval (200 tasks)
  4. Add all compiling, functionally valid children to archive
  5. After 80 generations, select the best-scoring agent from the archive
  6. Report that agent's SWE-bench Verified score on the 200-task evaluation set
- **Metrics**: Percentage of SWE-bench Verified tasks solved (out of 200), reported as a fraction (%)
- **Expected outcome**: DGM best agent outperforms the initial fixed agent on SWE-bench Verified; the gain is statistically meaningful relative to the initial agent's performance
- **Baselines**: Initial Claude 3.5 Sonnet agent (no self-improvement); human-engineered SWE-bench leaderboard systems
- **Dependencies**: none

## E02: DGM main evaluation on Polyglot (stability assessment)
- **Verifies**: C01
- **Setup**:
  - System: Full DGM (keep-all archive, score-child-proportional selection)
  - Self-modification LLM: Claude 3.5 Sonnet (New)
  - Coding agent LLM: o3-mini (`o3-mini-2025-01-31`) — different base model from E01
  - Dataset: Polyglot benchmark, 200-task subset; 60-task quick eval subset
  - Evolution: max_generation=80; run independently 3 times to assess stability
- **Procedure**:
  1. Initialize archive with initial o3-mini Polyglot agent
  2. Run DGM outer loop for 80 generations (same outer-loop hyperparameters as E01)
  3. Repeat 3 independent runs with different random seeds
  4. Report best-agent Polyglot score per run; also report mean and standard deviation across runs
- **Metrics**: Percentage of Polyglot tasks solved (out of 200); mean ± std across 3 runs
- **Expected outcome**: DGM outperforms initial o3-mini agent on Polyglot; results are stable across 3 runs (low std)
- **Baselines**: Initial o3-mini agent (no self-improvement); DGM ablation variants (from E03)
- **Dependencies**: none

## E03: Ablation study — open-ended exploration and self-improvement components
- **Verifies**: C02, C03, C04
- **Setup**:
  - Three ablation configurations:
    - (a) DGM w/o Open-ended exploration: archive retains only the single highest-scoring agent (greedy)
    - (b) DGM w/o Self-improve: archive-based exploration without LLM code modification (random or fixed initial agent as parent, no new code modifications)
    - (c) DGM Greedy: keep-all archive but deterministic best-parent selection (no novelty bonus)
  - Same LLMs, datasets, and compute budget as E01/E02 per benchmark
- **Procedure**:
  1. Run each ablation configuration for 80 generations on SWE-bench and Polyglot
  2. For each ablation, select the best agent from the final archive (or the single retained agent for w/o Open-ended)
  3. Evaluate best agent on 200-task SWE-bench and Polyglot sets
  4. Compare ablation scores to full DGM score from E01/E02
- **Metrics**: Percentage solved on SWE-bench Verified (200-task) and Polyglot (200-task); difference vs full DGM (pp drop)
- **Expected outcome**:
  - Removing open-ended exploration causes a larger performance drop than removing self-improvement
  - Keep-all archive (full DGM) outperforms greedy archive retention
  - Both components contribute positively; neither alone achieves full DGM performance
- **Baselines**: Full DGM (E01, E02)
- **Dependencies**: E01, E02

## E04: Agent functionality analysis across DGM and ablation variants
- **Verifies**: C05
- **Setup**:
  - All agent variants generated across DGM and ablation runs (SWE-bench setting)
  - Evaluation: test each agent for basic code-editing functionality (can the agent successfully edit files, run bash commands, and produce syntactically valid outputs)
  - Scope: all agents in the archive at end of run (DGM, DGM w/o Open-ended, DGM w/o Self-improve)
- **Procedure**:
  1. Collect all agents from each run's archive
  2. For each agent, run a basic functionality test: can it perform file editing and bash execution?
  3. Compute the fraction of agents with basic code-editing functionality per run
  4. Compare fractions across DGM and ablation variants
- **Metrics**: Percentage of generated agents with basic code-editing functionality (out of all agents in archive)
- **Expected outcome**: DGM produces a higher fraction of functionally capable agents than ablation variants; the gap reflects broader exploration of agent-code space
- **Baselines**: DGM w/o Open-ended, DGM w/o Self-improve (both reported at same fraction)
- **Dependencies**: E03

## E05: Hallucination-reduction case study via DGM
- **Verifies**: C06
- **Setup**:
  - System: DGM applied to a custom hallucination-reduction objective
  - Meta-LLM: Claude 3.5 Sonnet (New)
  - Dataset: 3 SWE-bench tasks (tiny subset, to reduce compute)
  - Custom evaluation metric: solve-hallucination score (0–2 scale: 0 = task not solved and hallucination present, 1 = either solved or no hallucination, 2 = both solved and no hallucination)
  - Evolution: 150 iterations
- **Procedure**:
  1. Define a custom solve-hallucination score for 3 SWE-bench tasks
  2. Run DGM for 150 iterations with this score as the fitness function
  3. Track all agents' hallucination scores across generations (Figure 8)
  4. Identify the best non-hacking agent (node 96) and the best hacking agent (node 114)
  5. Analyze node 114's code to identify the objective-hacking mechanism
  6. Report both scores and classify each as genuine improvement vs objective hacking
- **Metrics**: Solve-hallucination score (0–2, averaged over 3 tasks); binary classification of hacking vs genuine improvement
- **Expected outcome**: DGM discovers agents with higher hallucination scores than the initial agent; at least one agent engages in objective hacking (metric spoofing), demonstrating the dual nature of unconstrained self-improvement
- **Baselines**: Initial Claude 3.5 Sonnet agent (no hallucination mitigation)
- **Dependencies**: E01
