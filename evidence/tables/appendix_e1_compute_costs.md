# Table 4 — Estimated Compute Costs Per Experimental Configuration

**Source**: Appendix E.1 in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Approximate cost estimates for each DGM experimental configuration. Costs are in USD and are estimates.
**Extraction type**: raw_table
**Section**: Appendix E.1

| Configuration | Estimated Cost (USD) |
|--------------|---------------------|
| Full DGM run on SWE-bench | ~$22,000 |
| DGM w/o Self-improve on SWE-bench | ~$10,000 |
| DGM w/o Open-ended exploration on SWE-bench | ~$10,000 |
| Claude 3.5 Sonnet (New) on SWE-bench, 60 tasks (single eval) | $350 |
| o3-mini on Polyglot, 60 tasks (single eval) | $5 |

**Notes**:
- All cost estimates are approximate; actual costs depend on API pricing at time of experiment
- The $22K full DGM cost covers 80 generations × 2 self-improvement workers × (LLM API calls for diagnosis + coding agent + evaluation)
- Ablation runs (~$10K each) cost approximately half of full DGM because they either skip self-modification or skip open-ended exploration, reducing the number of distinct LLM calls
- The per-eval costs ($350 for SWE-bench 60 tasks, $5 for Polyglot 60 tasks) illustrate the large cost difference between Claude 3.5 Sonnet and o3-mini
- These costs make DGM accessible mainly to well-resourced research labs; rapid iteration requires using the 60-task quick-eval proxy
