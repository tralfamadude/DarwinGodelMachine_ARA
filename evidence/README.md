# Evidence Index

## Tables

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1_main_results.md](tables/table1_main_results.md) | Table 1, §4, Appendix A.3 | C01, C02, C03, C04 | Main results: DGM (50.0% SWE-bench, 38.0% Polyglot) vs three ablation variants |
| [tables/table2_agent_functionality.md](tables/table2_agent_functionality.md) | Table 2, Appendix A.4 | C05 | % of generated agents with basic code-editing functionality: DGM (51.3%) vs ablations (32.5%) |
| [tables/table3_foundation_models.md](tables/table3_foundation_models.md) | Table 3, Appendix D.1 | C01 | Foundation models per experiment: Claude 3.5 Sonnet for SWE-bench; o3-mini for Polyglot coding agent |
| [tables/appendix_e1_compute_costs.md](tables/appendix_e1_compute_costs.md) | Appendix E.1 | — | Estimated costs: ~$22K full DGM (SWE-bench), ~$10K ablations, $350 per 60-task Claude eval |
| [tables/derived_polyglot_stability.md](tables/derived_polyglot_stability.md) | Appendix B | C01 | Polyglot stability over 3 runs: mean 40.7%, std 2.3% (derived from Appendix B, not a numbered source table) |

## Figures

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure2_performance_curves.md](figures/figure2_performance_curves.md) | Figure 2, §4 | C01, C02, C03, C04 | Best-archive-agent performance over 80 DGM generations for all variants on SWE-bench and Polyglot |
| [figures/figure8_hallucination_archive.md](figures/figure8_hallucination_archive.md) | Figure 8, Appendix H | C06 | Archive solve-hallucination scores over 150 iterations; node 96 (1.67, genuine) and node 114 (2.0, hacking) |

## Claim-Evidence Cross-Reference

| Claim | Evidence files |
|-------|---------------|
| C01 (DGM achieves 50.0% / 38.0%) | table1_main_results.md, table3_foundation_models.md, figure2_performance_curves.md, derived_polyglot_stability.md |
| C02 (Open-ended exploration is primary driver) | table1_main_results.md (DGM w/o Open-ended row), figure2_performance_curves.md |
| C03 (Self-improvement contributes meaningfully) | table1_main_results.md (DGM w/o Self-improve row), figure2_performance_curves.md |
| C04 (Keep-all beats greedy) | table1_main_results.md (DGM Greedy row), figure2_performance_curves.md |
| C05 (DGM generates more functional agents) | table2_agent_functionality.md |
| C06 (Generalizes to hallucination; objective hacking risk) | figure8_hallucination_archive.md |
