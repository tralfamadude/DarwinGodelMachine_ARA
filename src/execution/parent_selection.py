"""
DGM Parent Selection: Score-Child-Proportional Method
Source: DGM_outer.py (choose_selfimproves function)
Paper: Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents
       arXiv:2505.22954

Implements Equations 1-6 from Appendix C.2:
  α_i = performance(a_i)                                   [Eq. 1]
  n_i = functioning_children_count(a_i)                   [Eq. 2]
  s_i = 1 / (1 + exp(-λ(α_i - α₀)))    λ=10, α₀=0.5     [Eq. 3]
  h_i = 1 / (1 + n_i)                                     [Eq. 4]
  w_i = s_i * h_i                                          [Eq. 5]
  p_i = w_i / Σ_j w_j                                     [Eq. 6]
"""

from __future__ import annotations

import math
import random
from typing import Sequence

# ---------------------------------------------------------------------------
# Core selection weight computation
# ---------------------------------------------------------------------------

def sigmoid_performance_weight(
    alpha: float,
    sigmoid_lambda: float = 10.0,
    sigmoid_alpha0: float = 0.5,
) -> float:
    """
    Compute sigmoid-scaled performance weight s_i for a single agent.

    s_i = 1 / (1 + exp(-λ(α_i - α₀))

    Args:
        alpha: Agent's task-solve rate in [0.0, 1.0].
        sigmoid_lambda: Sharpness parameter λ (default 10, from Appendix C.2).
        sigmoid_alpha0: Sigmoid midpoint α₀ (default 0.5, from Appendix C.2).

    Returns:
        Sigmoid-scaled performance weight in (0.0, 1.0).
    """
    return 1.0 / (1.0 + math.exp(-sigmoid_lambda * (alpha - sigmoid_alpha0)))


def novelty_bonus(functioning_children: int) -> float:
    """
    Compute novelty bonus h_i for a single agent.

    h_i = 1 / (1 + n_i)

    Penalizes agents that have already produced many functioning children,
    encouraging exploration of under-explored lineages.

    Args:
        functioning_children: Number of valid children n_i already spawned.

    Returns:
        Novelty bonus in (0.0, 1.0]; equals 1.0 when n_i = 0.
    """
    return 1.0 / (1.0 + functioning_children)


def compute_selection_weights(
    scores: Sequence[float],
    functioning_children_counts: Sequence[int],
    sigmoid_lambda: float = 10.0,
    sigmoid_alpha0: float = 0.5,
) -> list[float]:
    """
    Compute unnormalized selection weights w_i = s_i * h_i for each agent.

    Args:
        scores: Per-agent task-solve rates α_i in [0, 1].
        functioning_children_counts: Per-agent functioning children counts n_i.
        sigmoid_lambda: λ for sigmoid (default 10).
        sigmoid_alpha0: α₀ for sigmoid (default 0.5).

    Returns:
        List of unnormalized weights w_i; same length as input sequences.

    Raises:
        ValueError: If scores and functioning_children_counts have different lengths.
    """
    if len(scores) != len(functioning_children_counts):
        raise ValueError(
            f"scores (len={len(scores)}) and functioning_children_counts "
            f"(len={len(functioning_children_counts)}) must have equal length."
        )
    weights = []
    for alpha, n in zip(scores, functioning_children_counts):
        s = sigmoid_performance_weight(alpha, sigmoid_lambda, sigmoid_alpha0)
        h = novelty_bonus(n)
        weights.append(s * h)
    return weights


def normalize_weights(weights: list[float]) -> list[float]:
    """
    Normalize raw weights to a probability distribution.

    p_i = w_i / Σ_j w_j

    Args:
        weights: Unnormalized selection weights (must all be ≥ 0; at least one > 0).

    Returns:
        Normalized probabilities summing to 1.0.

    Raises:
        ValueError: If all weights are zero.
    """
    total = sum(weights)
    if total <= 0:
        raise ValueError("All weights are zero; cannot normalize.")
    return [w / total for w in weights]


def sample_parents(
    agent_ids: Sequence[str],
    scores: Sequence[float],
    functioning_children_counts: Sequence[int],
    k: int,
    method: str = "score_child_prop",
    sigmoid_lambda: float = 10.0,
    sigmoid_alpha0: float = 0.5,
    rng: random.Random | None = None,
) -> list[str]:
    """
    Sample k parent agent IDs from the eligible archive population.

    Implements the score-child-proportional selection described in Appendix C.2.
    Only agents with score < 1.0 are eligible.

    Args:
        agent_ids: IDs of agents in the eligible archive (those with α < 1.0).
        scores: Corresponding task-solve rates in [0.0, 1.0).
        functioning_children_counts: Corresponding functioning children counts.
        k: Number of parents to sample (with replacement).
        method: Selection method: 'score_child_prop' | 'score_prop' | 'random' | 'best'.
        sigmoid_lambda: λ for sigmoid scaling (default 10).
        sigmoid_alpha0: α₀ for sigmoid midpoint (default 0.5).
        rng: Optional random.Random instance for reproducibility.

    Returns:
        List of k sampled agent IDs (with replacement allowed).
    """
    if rng is None:
        rng = random.Random()

    ids = list(agent_ids)
    if not ids:
        return []

    if method == "best":
        best_id = ids[max(range(len(ids)), key=lambda i: scores[i])]
        return [best_id] * k

    if method == "random":
        return rng.choices(ids, k=k)

    # Compute weights
    raw_weights = compute_selection_weights(
        scores, functioning_children_counts,
        sigmoid_lambda=sigmoid_lambda,
        sigmoid_alpha0=sigmoid_alpha0,
    )

    if method == "score_prop":
        # Score-proportional only (no novelty bonus)
        score_weights = [
            sigmoid_performance_weight(alpha, sigmoid_lambda, sigmoid_alpha0)
            for alpha in scores
        ]
        norm = normalize_weights([max(w, 1e-10) for w in score_weights])
    else:
        # score_child_prop (default): use combined s_i * h_i weights
        norm = normalize_weights([max(w, 1e-10) for w in raw_weights])

    return rng.choices(ids, weights=norm, k=k)
