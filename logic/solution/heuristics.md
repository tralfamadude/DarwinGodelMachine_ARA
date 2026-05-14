# Heuristics

## H01: Two-phase evaluation (quick 60-task gate before full 200-task eval)
- **Rationale**: Full evaluation of 200 tasks per agent is expensive (~$350 for Claude 3.5 Sonnet on SWE-bench; ~$5 for o3-mini on Polyglot). Running quick eval first (60 tasks) filters out clearly low-quality children before spending on full evaluation. Only agents whose quick score exceeds a configurable threshold proceed to full eval.
- **Sensitivity**: medium — the quick-eval subset is a noisy proxy; variance on 60 tasks may misrank some agents. Too low a threshold wastes compute on low-quality agents; too high a threshold prunes valid improvements.
- **Bounds**: 60 tasks for quick eval; 200 tasks for full eval. Threshold value is configurable (`get_full_eval_threshold()` in `DGM_outer.py`).
- **Code ref**: [`src/execution/dgm_outer.py`](../execution/dgm_outer.py) (`get_full_eval_threshold()`), [`src/execution/dgm_outer.py`](../execution/dgm_outer.py) (`filter_compiled()`)
- **Source**: §3, Appendix A.1, A.2; repo `DGM_outer.py`

## H02: Sigmoid performance scaling for parent selection (λ=10, α₀=0.5)
- **Rationale**: Raw score-proportional selection would heavily favor already high-performing agents, causing premature convergence. The sigmoid transform $s_i = 1/(1 + \exp(-10(\alpha_i - 0.5)))$ compresses extreme scores (very low and very high performers get reduced weight), focusing selection pressure on mid-range performers with room to improve.
- **Sensitivity**: medium — $\lambda$ controls sharpness: $\lambda \to \infty$ approaches argmax (greedy), $\lambda \to 0$ approaches uniform sampling. $\alpha_0=0.5$ assumes the useful score range is centered at 50%.
- **Bounds**: $\lambda=10$, $\alpha_0=0.5$; output $s_i \in (0, 1)$.
- **Code ref**: [`src/execution/parent_selection.py`](../execution/parent_selection.py)
- **Source**: Appendix C.2; repo `DGM_outer.py` (`choose_selfimproves()`)

## H03: Novelty bonus to discourage over-exploited lineages (hᵢ = 1/(1+nᵢ))
- **Rationale**: Without a novelty penalty, parent selection converges to repeatedly improving the same high-performing lineage, reducing archive diversity and missing alternative evolutionary paths. The novelty bonus $h_i = 1/(1+n_i)$ geometrically penalizes agents that have already produced many children, encouraging exploration of under-explored lineages.
- **Sensitivity**: high — this term is the primary driver of diversity. If $h_i$ is removed (DGM Greedy variant), performance drops from 50.0% to 39.7% on SWE-bench. The $1/(1+n_i)$ form ensures the bonus decays quickly after the first few children but never reaches zero.
- **Bounds**: $h_i \in (0, 1]$; $h_i = 1$ for agents with no children, $h_i \to 0$ as $n_i \to \infty$.
- **Code ref**: [`src/execution/parent_selection.py`](../execution/parent_selection.py)
- **Source**: Appendix C.2; repo `DGM_outer.py` (`choose_selfimproves()`)

## H04: Keep-all archive (retain every valid agent regardless of score)
- **Rationale**: Greedy pruning (retaining only the best agent) eliminates evolutionary "stepping stones" — intermediate agents that score lower than current best but lie on paths to higher-scoring descendants. The ablation (DGM w/o Open-ended: greedy archive) scores 23.0% vs DGM's 50.0% on SWE-bench, confirming that diverse retention is essential.
- **Sensitivity**: high — the single most impactful design choice. Switching from keep-all to greedy causes the largest observed performance drop across all ablations.
- **Bounds**: Archive grows monotonically; an agent is retained if it compiles and has basic code-editing functionality (even if score = 0%). No upper bound on archive size within a run.
- **Code ref**: [`src/execution/dgm_outer.py`](../execution/dgm_outer.py) (`update_archive()`)
- **Source**: §3, Appendix C.1, ablation results (Table 1); repo `DGM_outer.py`

## H05: Docker isolation per evaluation with 9-hour timeout
- **Rationale**: Evaluating multiple agent variants in shared environments risks cross-contamination (e.g., one agent's file modifications affecting another's evaluation). Docker containers provide complete isolation. The 9-hour timeout accommodates the longest SWE-bench tasks without indefinitely blocking workers.
- **Sensitivity**: low — Docker isolation is a correctness requirement, not a tunable parameter. The 9-hour timeout is a generous bound; most evaluations complete faster.
- **Bounds**: Each agent-task pair runs in a fresh Docker container; containers are cleaned up after evaluation. `cleanup_container()` is called on success or failure.
- **Code ref**: [`src/execution/dgm_outer.py`](../execution/dgm_outer.py) (references docker_utils); actual implementation in `utils/docker_utils.py`
- **Source**: §3, Appendix A.1; repo `utils/docker_utils.py`, `swe_bench/harness.py`

## H06: Cumulative patch application from root ancestor
- **Rationale**: Storing full code copies for each agent variant would require O(N × codebase_size) storage. Instead, each agent stores only its delta (git diff) relative to its parent. Reconstruction applies all ancestor patches sequentially from the root. This approach also makes lineage relationships explicit and auditable.
- **Sensitivity**: low — correctness requirement. Patch conflicts would corrupt reconstruction; the implementation validates each `git apply` call. The constraint is that all ancestor patches must be conflict-free when applied sequentially (guaranteed by the sequential self-improvement process).
- **Bounds**: Patch depth = lineage depth (at most max_generation steps from root). Each patch is a standard unified diff (git format).
- **Code ref**: [`src/execution/dgm_outer.py`](../execution/dgm_outer.py) (calls `get_model_patch_paths`); actual implementation in `utils/git_utils.py`
- **Source**: §3; repo `utils/git_utils.py` (`get_model_patch_paths()`, `apply_patch()`)
