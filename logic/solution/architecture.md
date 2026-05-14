# Architecture

## System Overview

DGM is a two-level system: an **outer evolutionary loop** that manages a growing archive of agent variants and orchestrates self-improvement, and an **inner coding agent** that is the subject of self-modification and is evaluated on software engineering benchmarks.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DGM Outer Loop                               │
│                        (DGM_outer.py)                               │
│                                                                     │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐   │
│  │   Archive    │───▶│ Parent Selector  │───▶│ Self-Improvement │   │
│  │   Manager   │◀───│ (score-child-prop)│    │    Workers       │   │
│  └──────────────┘    └─────────────────┘    └──────────┬───────┘   │
│         ▲                                               │            │
│         └───────────────────────────────────────────────┘           │
│                    (add valid children)                              │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Self-Improvement Worker                             │
│                 (self_improve_step.py)                               │
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────────────────┐ │
│  │   Patch      │    │   Meta-LLM   │    │   Docker Container    │ │
│  │   Rebuilder  │───▶│  (Diagnosis) │───▶│   (Coding Agent)      │ │
│  │ (git_utils)  │    │   llm.py     │    │   coding_agent.py     │ │
│  └──────────────┘    └──────────────┘    └───────────┬───────────┘ │
│                                                        │             │
│                             ┌──────────────────────────┘             │
│                             ▼                                        │
│                     ┌──────────────┐    ┌───────────────────────┐  │
│                     │  Evaluator   │───▶│   Benchmark Harness   │  │
│                     │  (60→200     │    │  swe_bench/harness.py │  │
│                     │   tasks)     │    │  polyglot/harness.py  │  │
│                     └──────────────┘    └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. DGM Outer Loop
- **File**: `DGM_outer.py`
- **Purpose**: Top-level evolutionary controller; manages generations, archive, and worker coordination
- **Inputs**: Initial agent code, max_generation, selfimprove_size, selfimprove_workers, choose_selfimproves_method, update_archive strategy
- **Outputs**: Saved archive JSONL (metadata per agent), final archive of agent variants
- **Key design choices**: Parallel workers using Python multiprocessing; checkpointing via JSONL append; supports resuming from interrupted runs
- **Interactions**: Calls Parent Selector, spawns Self-Improvement Workers, calls Archive Manager

### 2. Archive Manager
- **File**: `DGM_outer.py` (`update_archive()`, `initialize_run()`, `filter_compiled()`)
- **Purpose**: Maintains the set of all valid agent variants; supports keep-all and greedy update strategies
- **Inputs**: Set of child agents from current generation (with scores)
- **Outputs**: Updated archive $A^{t+1}$
- **Key design choices**: keep-all (default) retains every agent with basic functionality; greedy retains only the single highest scorer; agents stored as metadata pointers to patch files on disk
- **Interactions**: Called by DGM Outer Loop after each generation

### 3. Parent Selector
- **File**: `DGM_outer.py` (`choose_selfimproves()`)
- **Purpose**: Implements score-child-proportional selection to sample parent agents from the archive
- **Inputs**: Current archive $A^t$ with per-agent scores and child counts; selection method flag
- **Outputs**: List of $k$ (parent, task) pairs to process in the next generation
- **Key design choices**: Sigmoid scaling ($\lambda=10$, $\alpha_0=0.5$) to smooth score-proportional selection; novelty bonus $h_i = 1/(1+n_i)$ discourages re-exploring over-exploited lineages; $k=2$ for SWE-bench, $k=4$ for Polyglot
- **Interactions**: Called by DGM Outer Loop at start of each generation

### 4. Self-Improvement Worker
- **File**: `self_improve_step.py`
- **Purpose**: Implements a single self-improvement attempt: diagnose → modify → evaluate → report
- **Inputs**: Parent agent metadata (lineage, patch paths, score), failing task τ
- **Outputs**: Child agent metadata (score, patches) or failure indicator
- **Key design choices**: Docker isolation per evaluation; 9-hour timeout; stochastic failure returns ∅; cumulative patch application reconstructs full code from lineage
- **Interactions**: Calls Patch Rebuilder, Meta-LLM, Coding Agent (inside Docker), Evaluator

### 5. Patch Rebuilder
- **File**: `utils/git_utils.py` (`get_model_patch_paths()`, `apply_patch()`)
- **Purpose**: Reconstructs any agent's source code by replaying all ancestor git patches from root
- **Inputs**: Agent lineage (list of ancestor patch file paths)
- **Outputs**: Full agent source code (codebase directory ready for Docker injection)
- **Key design choices**: Uses `git apply` for patch application; validates each patch application; untracked files included in diffs; full initial codebase as root
- **Interactions**: Called by Self-Improvement Worker before diagnosis and Docker launch

### 6. Meta-LLM (Diagnosis + Proposal)
- **File**: `llm.py`, `llm_withtools.py`, `prompts/self_improvement_prompt.py`
- **Purpose**: Analyzes failing task execution logs and proposes a concrete code modification to the coding agent
- **Inputs**: Current agent codebase (as string), failing task description, execution log, test results
- **Outputs**: JSON improvement proposal containing the proposed code modification and rationale
- **Key design choices**: Uses Claude 3.5 Sonnet (New) for both benchmarks; structured JSON output via `extract_json_between_markers()`; special prompts for edge cases (empty patches, stochastic failures, context-length issues); `get_current_code()` assembles full agent code from patches before prompting
- **Interactions**: Called by Self-Improvement Worker; uses Anthropic/OpenAI APIs via `llm.py`

### 7. Coding Agent (Inner)
- **File**: `coding_agent.py` (SWE-bench), `coding_agent_polyglot.py` (Polyglot)
- **Purpose**: The agent being evolved; solves benchmark tasks using LLM with tool use (bash, editor)
- **Inputs**: Task problem statement, test description
- **Outputs**: Code patch solving the task; optionally runs regression tests
- **Key design choices**: Claude 3.5 Sonnet (New) for SWE-bench tasks; o3-mini for Polyglot tasks; tools: `bash` (persistent asyncio session), `editor` (view/create/edit commands); `AgenticSystem.forward()` implements tool-calling loop
- **Interactions**: Runs inside Docker container launched by Self-Improvement Worker; evolved via patches applied by Patch Rebuilder

### 8. Benchmark Evaluator / Harness
- **Files**: `swe_bench/harness.py`, `polyglot/harness.py`, `test_swebench.py`
- **Purpose**: Runs the coding agent against benchmark tasks, collects patches, and scores pass/fail
- **Inputs**: Coding agent code, task list, Docker configuration
- **Outputs**: Per-task pass/fail results; overall solve rate (%)
- **Key design choices**: Each task runs in an isolated Docker container; SWE-bench harness parallelizes across tasks with configurable worker count; 9-hour timeout per agent; two-phase evaluation (quick 60-task → full 200-task)
- **Interactions**: Called by Self-Improvement Worker (for per-agent eval) and by DGM Outer Loop (for final archive eval)

### 9. Docker Environment Manager
- **File**: `utils/docker_utils.py`
- **Purpose**: Manages Docker container lifecycle for isolated agent evaluation
- **Inputs**: Container configuration, agent code to inject
- **Outputs**: Running Docker container; execution logs
- **Key design choices**: Thread-safe logging; copy-in/copy-out for agent code and results; automatic cleanup; `build_dgm_container()` builds the base image from Dockerfile (Python 3.10-slim)
- **Interactions**: Called by Self-Improvement Worker and Benchmark Evaluator
