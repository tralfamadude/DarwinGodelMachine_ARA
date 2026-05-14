# Table 1 — Main Experimental Results: DGM vs Ablations

**Source**: Table 1 in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Performance comparison of DGM and ablation variants on SWE-bench Verified (200-task subset) and Polyglot (200-task subset). Scores are reported as percentage of tasks solved.
**Extraction type**: raw_table
**Section**: §4 (Experiments), Appendix A.3 (Extended Results)

| Method | SWE-bench (%) | Polyglot (%) |
|--------|--------------|-------------|
| DGM (full system) | 50.0 | 38.0 |
| DGM w/o Open-ended exploration | 23.0 | 14.0 |
| DGM w/o Self-improve | 39.0 | 28.0 |
| DGM Greedy | 39.7 | 30.0 |

**Notes**:
- DGM Greedy = keep-all archive but deterministic best-parent selection (no novelty bonus / open-ended diversity mechanism)
- DGM w/o Open-ended exploration = greedy archive retaining only the single highest-scoring agent
- DGM w/o Self-improve = archive-based exploration without LLM code modification (no self-improvement)
- Polyglot DGM stability (3 independent runs): mean 40.7%, std 2.3% (Appendix B) — the 38.0% is from a representative single run reported in the main table
- All evaluations use the best agent from the archive at the end of training (80 generations)
- SWE-bench setting: Claude 3.5 Sonnet (New) for both self-modification and coding agent evaluation
- Polyglot setting: Claude 3.5 Sonnet (New) for self-modification; o3-mini for coding agent evaluation
