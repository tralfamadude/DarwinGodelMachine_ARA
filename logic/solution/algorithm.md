# Algorithm

## Mathematical Formulation

### Archive and Agent Representation

Let $a^0$ denote the initial coding agent (root of all lineages). At generation $t$, the archive is:

$$A^t = \{a^1_t, a^2_t, \ldots, a^N_t\}$$

Each agent $a^i$ is associated with:
- $\alpha_i \in [0,1]$: task-solve rate (performance on benchmark evaluation)
- $n_i \in \mathbb{Z}_{\geq 0}$: number of functioning children spawned from $a^i$
- $\Pi_i = (a^{p_1}, a^{p_2}, \ldots, a^{p_d}, a^i)$: ancestry chain (lineage from root to $a^i$)
- code($a^i$) = apply(patches($\Pi_i$), code($a^0$)): reconstructed source code

### Parent Selection (Score-Child-Proportional)

Eligible set at generation $t$:

$$E^t = \{a^i \in A^t : \alpha_i < 1\}$$

For each $a^i \in E^t$, compute unnormalized weight:

$$s_i = \frac{1}{1 + \exp(-\lambda(\alpha_i - \alpha_0))}, \quad \lambda = 10,\; \alpha_0 = 0.5 \tag{sigmoid performance}$$

$$h_i = \frac{1}{1 + n_i} \tag{novelty bonus}$$

$$w_i = s_i \cdot h_i \tag{combined weight}$$

Selection probability:

$$p_i = \frac{w_i}{\sum_{j \in E^t} w_j} \tag{normalized}$$

Draw $k$ parents (with replacement) from $E^t$ according to $\{p_i\}$.

### Empirical Validation (two-phase)

Let eval($a^i$, $\mathcal{T}$) denote the task-solve rate on task set $\mathcal{T}$:

$$\text{quick\_score}_i = \text{eval}(a^i, \mathcal{T}_{60}) \quad (|\mathcal{T}_{60}| = 60\text{ tasks})$$

$$\alpha_i = \text{eval}(a^i, \mathcal{T}_{200}) \quad \text{if quick\_score}_i > \theta_{\text{threshold}}$$

### Stability Measure

For Polyglot (3 independent runs $r = 1, 2, 3$):

$$\mu = \frac{1}{3}\sum_{r=1}^{3} \alpha^*_r, \quad \sigma = \sqrt{\frac{1}{3}\sum_{r=1}^{3}(\alpha^*_r - \mu)^2}$$

where $\alpha^*_r = \max_{a^i \in A^{80}_r} \alpha_i$ is the best agent score in run $r$.

---

## Pseudocode

```
Algorithm: Darwin Gödel Machine (DGM)

Input:
  a₀:             initial coding agent
  T:              max_generation (= 80)
  k:              selfimprove_size (= 2 for SWE-bench, = 4 for Polyglot)
  W:              selfimprove_workers (= 2)
  λ = 10, α₀ = 0.5:  sigmoid parameters
  θ:              quick-eval pass threshold

Initialize:
  A = {a₀}
  score(a₀) = eval(a₀, T₂₀₀)
  children_count(a₀) = 0

For t = 1, ..., T:
  # --- Parent Selection ---
  E = {aᵢ ∈ A : αᵢ < 1}
  For each aᵢ ∈ E:
    sᵢ = sigmoid(λ(αᵢ - α₀))
    hᵢ = 1 / (1 + nᵢ)
    wᵢ = sᵢ × hᵢ
  pᵢ = wᵢ / Σⱼ wⱼ
  parents = sample(E, k, probabilities=p)

  # --- Parallel Self-Improvement ---
  children = []
  Parallel (W workers):
    For each parent aⱼ in parents:
      # Reconstruct code
      code_j = apply_patches(ancestry(aⱼ), code(a₀))

      # Diagnose and propose modification
      τ = sample_failing_task(benchmark)
      proposal = meta_llm.diagnose_and_propose(code_j, τ)

      # Implement in Docker
      code_child = run_coding_agent_in_docker(code_j, proposal)

      # Evaluate
      q_score = eval(code_child, T₆₀)
      If q_score > θ:
        α_child = eval(code_child, T₂₀₀)
      Else:
        α_child = q_score

      # Validity check
      If code_child.compiles() AND has_basic_functionality(code_child):
        child = create_agent(code_child, α_child, parent=aⱼ)
        children.append(child)
        children_count(aⱼ) += 1

  # --- Archive Update (keep-all) ---
  A = A ∪ children

  # --- Checkpoint ---
  save_archive_metadata(A, t)

Return: argmax_{aᵢ ∈ A} αᵢ  # best agent from final archive
```

### Self-Improvement Step (inner)

```
Function: self_improve_step(parent aⱼ, task τ)

1. Reconstruct: code_j = apply_patches(ancestry(aⱼ), code(a₀))
2. Build Docker container with code_j
3. meta_prompt = build_diagnose_prompt(code_j, τ, execution_log)
4. proposal = call_llm(meta_llm, meta_prompt) → JSON
5. patch = coding_agent_in_docker(code_j, proposal, τ)
6. code_child = apply(patch, code_j)
7. q_score = eval(code_child, T₆₀)
8. If q_score > θ: α_child = eval(code_child, T₂₀₀)
9. If compiles(code_child) AND functional(code_child):
     Return new_agent(code_child, α_child, parent=aⱼ)
10. Else: Return ∅
```

---

## Complexity Analysis

| Component | Complexity per generation |
|-----------|--------------------------|
| Parent selection | O(N) where N = archive size |
| Archive update | O(k) per generation |
| Self-improvement (per child) | O(L × D × E) where L = LLM call count, D = Docker setup, E = eval tasks |
| Total compute (dominant) | O(T × k × (LLM + eval)) |

**Practical bottleneck**: LLM API calls and benchmark evaluation (Docker+9h timeout). Archive management and parent selection are negligible relative to evaluation cost.

**Total compute**: ~$22,000 USD per full DGM SWE-bench run (80 generations × 2 parents × ~$22K amortized LLM + eval costs).

---

## Key Algorithmic Properties

1. **Monotonic archive growth**: Archive never shrinks under keep-all strategy; every valid child is retained indefinitely.
2. **Lineage tracking**: Every agent has a full ancestry chain; reconstruction is deterministic given patch files.
3. **Score-proportional with novelty**: Sigmoid scaling concentrates selection pressure on mid-range performers; novelty bonus prevents runaway exploitation of any single lineage.
4. **Two-phase evaluation**: 60-task quick eval gates expensive 200-task full eval, reducing wasted compute on low-quality children.
5. **Parallelism**: W workers run simultaneously per generation; children are independent (no shared state during self-improvement).
