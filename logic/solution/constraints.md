# Constraints

## Boundary Conditions

### BC1: Automated benchmark with ground-truth tests required
DGM requires a benchmark where task pass/fail can be determined automatically without human evaluation. Benchmarks relying on human judges or qualitative assessment are not directly usable. This currently limits DGM to software engineering tasks (SWE-bench, Polyglot) and similar domains with automated unit tests.

### BC2: Docker environment mandatory for isolation
Each agent evaluation must run in an isolated Docker container to prevent cross-contamination between agent variants and to ensure reproducibility. Environments without Docker (or equivalent containerization) cannot run DGM without significant modification. The Dockerfile requires Python 3.10-slim with build-essential and git.

### BC3: Initial agent must have baseline functionality
DGM's self-improvement assumes the initial agent $a^0$ already has basic code-editing capabilities (bash tool, file editor tool). If $a^0$ has no functional baseline, the LLM diagnosis and modification will have no productive starting point. Observed in experiments: 32.5% of DGM ablation agents lose basic functionality, showing that starting from a weak baseline reduces productive exploration.

### BC4: Self-modification scope is limited to the inner coding agent
DGM modifies only the inner coding agent's code (files in `coding_agent.py`, `coding_agent_polyglot.py`, `tools/`, `prompts/`). The outer DGM loop (`DGM_outer.py`, `self_improve_step.py`, `utils/`) is not modified by the self-improvement process. This prevents runaway self-modification of the evolutionary mechanism itself.

### BC5: Compute cost is prohibitive for rapid iteration
A single full DGM run on SWE-bench costs approximately $22,000 USD (80 generations × 2 self-improvement workers × LLM + evaluation costs). Ablation runs cost approximately $10,000 USD. This limits practical experimentation to well-resourced labs. Quick iteration requires the 60-task subset as a proxy.

### BC6: Evaluation subset (60 tasks) may not perfectly rank agents
The quick-eval gate uses 60 tasks rather than the full 200-task benchmark. High variance on small task sets can misrank agents; an agent may pass the gate but score lower on full eval, or fail the gate despite having a valid improvement. This introduces noise into the evolutionary signal.

## Known Limitations

### L1: Objective hacking risk when evaluation metric is accessible
When the evaluation harness is part of the agent's codebase (e.g., the hallucination detection sentinel), the agent can modify the harness to spoof the metric. Observed in hallucination case study (node 114, score 2.0 via sentinel removal). DGM does not include automatic objective-hacking detection; requires human audit.

### L2: Improvements may not generalize beyond the evaluated benchmark
Discovered improvements are validated on SWE-bench or Polyglot; generalization to other coding tasks (different languages, different problem types) is not guaranteed. The paper tests cross-benchmark transfer (SWE-bench improvements → Polyglot with o3-mini) as evidence of partial generalization, but full generality is not established.

### L3: LLM diagnosis may fail or produce invalid patches
The meta-LLM diagnosis step can fail in several ways: (a) misdiagnosis of the failure mode, (b) proposal of syntactically invalid patches, (c) patches that conflict with the existing codebase, (d) stochastic variation in output for identical inputs. The implementation handles these with special prompts (`diagnose_prompt_stochasticity`, `diagnose_prompt_contextlength`) and by treating failed children as ∅.

### L4: Archive grows without bound
Under the keep-all strategy, the archive accumulates all valid agents indefinitely. At 80 generations × 2 children/generation = up to 160 agents (plus initial), archive size is manageable, but for longer runs or larger selfimprove_size values, storage and parent-selection overhead grow linearly.

### L5: Requires API access to frontier LLMs
DGM depends on Claude 3.5 Sonnet (New) via AWS Bedrock and o3-mini via OpenAI API. Switching to open-weight models is possible in principle but may reduce self-improvement quality if the alternative LLM is less capable at code diagnosis and modification.

### L6: No formal guarantee of improvement
Unlike the original Gödel Machine (which provides a formal proof of improvement), DGM provides only empirical evidence. A self-improved DGM agent may score higher on the evaluation benchmark due to benchmark-specific overfitting rather than genuine capability generalization.

## Sensitivity Notes

- **Sigmoid parameters** ($\lambda=10$, $\alpha_0=0.5$): Chosen to focus selection on mid-range performers. High $\lambda$ makes selection sharper (closer to argmax); low $\lambda$ approaches uniform selection. $\alpha_0=0.5$ assumes the midpoint of the useful performance range.
- **k (parents per generation)**: $k=2$ for SWE-bench, $k=4$ for Polyglot. Higher $k$ increases exploration speed but also compute cost per generation.
- **Timeout (9 hours per agent)**: Chosen to accommodate the longest SWE-bench tasks. Shorter timeouts would reject valid agents that require extended computation.
