# Derived Subset — Polyglot Stability Results

**Source**: Derived from Appendix B in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Polyglot performance across 3 independent DGM runs (stability analysis). The main Table 1 reports a single representative run; Appendix B provides the stability statistics.
**Extraction type**: derived_subset
**Derived from**: Appendix B (DGM Polyglot stability), not a separately numbered table in the source

| Statistic | Value |
|-----------|-------|
| Run 1 (representative, reported in Table 1) | 38.0% |
| Mean across 3 runs | 40.7% |
| Standard deviation across 3 runs | 2.3% |

**Notes**:
- The mean (40.7%) is slightly higher than the Table 1 representative run (38.0%), indicating the representative run was slightly below average
- Standard deviation of 2.3% over 3 independent runs confirms DGM's stability — results are not single-run lucky outcomes
- All runs use the same configuration: Claude 3.5 Sonnet (New) for self-modification, o3-mini for Polyglot coding agent evaluation

**Claims supported**: C01 (stability component)
