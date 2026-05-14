# Figure 2 — DGM Performance Over Generations (SWE-bench and Polyglot)

**Source**: Figure 2 in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Performance of the best agent in the archive over DGM generations, for SWE-bench (top) and Polyglot (bottom). Shows full DGM vs ablation variants.
**Extraction type**: figure_data
**Section**: §4

**Axes**: X = DGM generation (0 to ~80), Y = best agent task-solve rate (%)

## Qualitative Data Points (Approximate Readings from Figure)

The figure shows performance curves for DGM (full), DGM w/o Open-ended, DGM w/o Self-improve, and DGM Greedy. Exact intermediate values are not reported in tabular form; only final values are precisely reported (see Table 1).

### SWE-bench Curves (approximate trajectory descriptions)

| Configuration | Gen 0 (initial) | Gen ~20 | Gen ~40 | Gen 80 (final) |
|--------------|----------------|---------|---------|----------------|
| DGM (full) | ≈39–40% | ≈42–44% | ≈45–47% | 50.0% |
| DGM w/o Open-ended | ≈39–40% | ≈40–42% | ≈42–43% | 23.0% (drops after peak) |
| DGM w/o Self-improve | ≈39–40% | ≈39–41% | ≈39–40% | 39.0% |
| DGM Greedy | ≈39–40% | ≈40–42% | ≈40–42% | 39.7% |

**Note**: Intermediate generation values are ≈ (approximate visual reads from figure); only final values (Gen 80) are exact per Table 1.

### Polyglot Curves (approximate trajectory descriptions)

| Configuration | Gen 0 (initial) | Gen ~20 | Gen ~40 | Gen 80 (final) |
|--------------|----------------|---------|---------|----------------|
| DGM (full) | ≈28–30% | ≈30–33% | ≈33–36% | 38.0% |
| DGM w/o Open-ended | ≈28–30% | ≈28–30% | ≈20–25% | 14.0% |
| DGM w/o Self-improve | ≈28–30% | ≈28–30% | ≈28–30% | 28.0% |
| DGM Greedy | ≈28–30% | ≈29–31% | ≈29–31% | 30.0% |

**Key observations from figure**:
- Full DGM shows monotonically increasing best-agent score with no performance regression
- DGM w/o Open-ended shows early peak then decline, consistent with premature convergence followed by loss of diversity
- DGM w/o Self-improve remains near the initial agent's performance throughout
- DGM Greedy improves moderately but plateaus below full DGM

**Precise final values** are available in [Table 1](../tables/table1_main_results.md).
