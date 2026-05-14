# Table 2 — Agent Functionality Analysis

**Source**: Table 2 in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Percentage of generated agents with basic code-editing functionality across DGM and ablation variants (SWE-bench setting).
**Extraction type**: raw_table
**Section**: Appendix A.4

| Method | % Agents with Basic Code-Editing Functionality |
|--------|-----------------------------------------------|
| DGM (full system) | 51.3 |
| DGM w/o Open-ended exploration | 32.5 |
| DGM w/o Self-improve | 32.5 |

**Notes**:
- "Basic code-editing functionality" = agent can successfully perform file editing and bash command execution (the minimum required for solving SWE-bench tasks)
- Percentages are computed over all agents generated and added to the archive during training (not just the best agent)
- DGM w/o Open-ended and DGM w/o Self-improve both produce exactly 32.5% functional agents, suggesting the two components contribute to functionality independently
- A ~19 pp gap (51.3% vs 32.5%) between DGM and ablations reflects broader code-space exploration under open-ended evolution
