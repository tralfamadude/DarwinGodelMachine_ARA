"""
DGM Outer Evolutionary Loop — Minimal Core Stub
Source: DGM_outer.py (https://github.com/jennyzzt/dgm)
Paper: Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents
       arXiv:2505.22954

This stub captures the novel evolutionary loop logic:
archive initialization, parent selection dispatch, parallel self-improvement,
archive update, and checkpointing.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class AgentMetadata:
    """Metadata record for a single agent variant in the archive."""
    agent_id: str                  # Unique identifier (e.g., "gen03_child01")
    parent_id: Optional[str]       # ID of the parent agent; None for root
    patch_path: Optional[str]      # Path to the git diff patch file (relative to run dir)
    score: float                   # Task-solve rate on full 200-task eval; in [0.0, 1.0]
    quick_score: float             # Task-solve rate on 60-task quick eval
    compiled: bool                 # Did the agent compile and pass basic functionality test?
    generation: int                # DGM generation in which this agent was created
    functioning_children: int = 0  # Number of valid children spawned from this agent


@dataclass
class DGMArchive:
    """
    Keep-all archive: retains all valid agent variants.
    Under the 'keep_all' update strategy, agents are never removed.
    Under 'greedy', only the single highest-scoring agent is retained.
    """
    agents: list[AgentMetadata] = field(default_factory=list)
    update_strategy: Literal["keep_all", "greedy"] = "keep_all"

    def add(self, agent: AgentMetadata) -> None:
        """Add an agent to the archive (always, under keep_all; conditionally under greedy)."""
        if self.update_strategy == "keep_all":
            self.agents.append(agent)
        elif self.update_strategy == "greedy":
            if not self.agents or agent.score > max(a.score for a in self.agents):
                self.agents = [agent]

    def best(self) -> Optional[AgentMetadata]:
        """Return the highest-scoring agent in the archive."""
        return max(self.agents, key=lambda a: a.score) if self.agents else None

    def eligible(self) -> list[AgentMetadata]:
        """Return agents with score < 1.0 (not yet perfect solvers)."""
        return [a for a in self.agents if a.score < 1.0]


# ---------------------------------------------------------------------------
# Parent selection: score-child-proportional
# ---------------------------------------------------------------------------

def select_parents(
    archive: DGMArchive,
    k: int,
    method: Literal["score_child_prop", "best", "random", "score_prop"] = "score_child_prop",
    sigmoid_lambda: float = 10.0,
    sigmoid_alpha0: float = 0.5,
) -> list[AgentMetadata]:
    """
    Select k parent agents from the eligible archive population.

    score_child_prop (default):
        w_i = s_i * h_i
        s_i = sigmoid(lambda * (alpha_i - alpha_0))   [performance term]
        h_i = 1 / (1 + n_i)                          [novelty bonus]
        p_i = w_i / sum(w_j)                          [selection probability]

    Args:
        archive: Current archive of agent variants.
        k: Number of parents to select (selfimprove_size).
        method: Selection algorithm.
        sigmoid_lambda: Sharpness parameter λ for sigmoid (default 10).
        sigmoid_alpha0: Midpoint α₀ for sigmoid (default 0.5).

    Returns:
        List of k selected parent AgentMetadata objects (with replacement).
    """
    import math

    eligible = archive.eligible()
    if not eligible:
        return []

    if method == "best":
        best = max(eligible, key=lambda a: a.score)
        return [best] * k

    if method == "random":
        return random.choices(eligible, k=k)

    if method in ("score_prop", "score_child_prop"):
        weights: list[float] = []
        for agent in eligible:
            alpha = agent.score
            s = 1.0 / (1.0 + math.exp(-sigmoid_lambda * (alpha - sigmoid_alpha0)))
            if method == "score_child_prop":
                h = 1.0 / (1.0 + agent.functioning_children)
                w = s * h
            else:
                w = s
            weights.append(max(w, 1e-10))  # avoid zero weights
        return random.choices(eligible, weights=weights, k=k)

    raise ValueError(f"Unknown method: {method}")


# ---------------------------------------------------------------------------
# Self-improvement step (stub — actual implementation in self_improve_step.py)
# ---------------------------------------------------------------------------

def run_self_improve_step(
    parent: AgentMetadata,
    run_dir: Path,
    benchmark: Literal["swe_bench", "polyglot"],
    quick_eval_tasks: int = 60,
    full_eval_tasks: int = 200,
) -> Optional[AgentMetadata]:
    """
    Execute one self-improvement attempt for a given parent agent.

    Steps (see self_improve_step.py for full implementation):
    1. Reconstruct parent code via cumulative patch application.
    2. Launch Docker container with reconstructed code.
    3. Meta-LLM diagnoses failing task and proposes modification.
    4. Coding agent implements modification inside Docker.
    5. Run quick eval (60 tasks); if score > threshold, run full eval (200 tasks).
    6. Return new AgentMetadata if child compiles and is functional; else None.

    Args:
        parent: Parent agent metadata.
        run_dir: Root directory containing patch files and logs.
        benchmark: Which benchmark to evaluate on.
        quick_eval_tasks: Number of tasks for quick evaluation gate.
        full_eval_tasks: Number of tasks for full evaluation.

    Returns:
        AgentMetadata for the new child agent, or None if self-improvement failed.
    """
    # NOTE: Full implementation delegates to self_improve_step.py
    # This stub shows the interface contract.
    raise NotImplementedError(
        "Delegate to self_improve_step.run_self_improve_step() in the actual implementation."
    )


# ---------------------------------------------------------------------------
# Main evolutionary loop
# ---------------------------------------------------------------------------

def run_dgm(
    run_dir: Path,
    initial_agent: AgentMetadata,
    max_generation: int = 80,
    selfimprove_size: int = 2,
    selfimprove_workers: int = 2,
    choose_method: Literal["score_child_prop", "best", "random", "score_prop"] = "score_child_prop",
    update_strategy: Literal["keep_all", "greedy"] = "keep_all",
    benchmark: Literal["swe_bench", "polyglot"] = "swe_bench",
    sigmoid_lambda: float = 10.0,
    sigmoid_alpha0: float = 0.5,
) -> AgentMetadata:
    """
    DGM outer evolutionary loop.

    Args:
        run_dir: Directory for saving checkpoints, patches, and metadata.
        initial_agent: Seed agent (a₀) with baseline score.
        max_generation: Number of evolutionary generations (T = 80).
        selfimprove_size: Parents selected per generation (k = 2 SWE-bench, 4 Polyglot).
        selfimprove_workers: Parallel workers for self-improvement (W = 2).
        choose_method: Parent selection algorithm.
        update_strategy: Archive update strategy ('keep_all' or 'greedy').
        benchmark: Benchmark to optimize on.
        sigmoid_lambda: λ for sigmoid performance scaling (default 10).
        sigmoid_alpha0: α₀ for sigmoid midpoint (default 0.5).

    Returns:
        The best-performing agent found across all generations.
    """
    archive = DGMArchive(update_strategy=update_strategy)
    archive.add(initial_agent)
    metadata_log = run_dir / "archive_metadata.jsonl"

    for generation in range(1, max_generation + 1):
        # --- Parent selection ---
        parents = select_parents(
            archive, k=selfimprove_size, method=choose_method,
            sigmoid_lambda=sigmoid_lambda, sigmoid_alpha0=sigmoid_alpha0,
        )
        if not parents:
            break  # All agents are perfect solvers or archive is empty

        # --- Parallel self-improvement ---
        children: list[AgentMetadata] = []
        with ProcessPoolExecutor(max_workers=selfimprove_workers) as executor:
            futures = {
                executor.submit(run_self_improve_step, parent, run_dir, benchmark): parent
                for parent in parents
            }
            for future in as_completed(futures):
                child = future.result()
                if child is not None:
                    children.append(child)
                    # Update parent's functioning_children count
                    parent_ref = futures[future]
                    parent_ref.functioning_children += 1

        # --- Archive update ---
        for child in children:
            archive.add(child)

        # --- Checkpoint ---
        with metadata_log.open("a") as f:
            for agent in children:
                f.write(json.dumps({
                    "generation": generation,
                    "agent_id": agent.agent_id,
                    "parent_id": agent.parent_id,
                    "score": agent.score,
                    "compiled": agent.compiled,
                }) + "\n")

    best = archive.best()
    assert best is not None, "Archive is empty after DGM run."
    return best
