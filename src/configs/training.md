# Training Configuration

## max_generation
- **Value**: 80
- **Rationale**: Provides sufficient generations for meaningful evolutionary exploration within a single run's compute budget (~$22K for SWE-bench). Chosen empirically; not ablated in the paper.
- **Search range**: Not specified in paper
- **Sensitivity**: medium — more generations allow further improvement but increase cost linearly
- **Source**: `DGM_outer.py` argparse defaults; §3

## selfimprove_size (k — parents per generation)
- **Value**: 2 (SWE-bench), 4 (Polyglot)
- **Rationale**: Number of parent agents selected per generation, each spawning one self-improvement attempt. Higher k for Polyglot provides more exploration diversity given the multi-language setting.
- **Search range**: Not specified in paper
- **Sensitivity**: medium — scales compute linearly; higher k increases diversity per generation
- **Source**: `DGM_outer.py` argparse defaults; Appendix A.1 (SWE-bench), Appendix A.2 (Polyglot)

## selfimprove_workers (W — parallel workers)
- **Value**: 2
- **Rationale**: Number of parallel processes running self-improvement steps simultaneously. Matches selfimprove_size for SWE-bench (all k attempts run in parallel). Limited by available API rate limits and Docker resources.
- **Search range**: Not specified in paper
- **Sensitivity**: low (for correctness); affects wall-clock time but not algorithm behavior
- **Source**: `DGM_outer.py` argparse defaults

## choose_selfimproves_method
- **Value**: `score_child_prop` (score-child-proportional)
- **Rationale**: Implements parent selection with sigmoid performance scaling and novelty bonus. Ablations compare against `best` (greedy) and uniform random.
- **Search range**: {`random`, `score_prop`, `score_child_prop`, `best`}
- **Sensitivity**: high — switching from `score_child_prop` to `best` drops SWE-bench from 50.0% to 39.7%; removing `score_child_prop` component entirely (w/o open-ended) drops to 23.0%
- **Source**: `DGM_outer.py` argparse; Appendix C.2; ablation results (Table 1)

## update_archive
- **Value**: `keep_all`
- **Rationale**: Retains all valid agents in the archive regardless of score, preserving evolutionary diversity and stepping stones. Alternative `greedy` (keep only best) causes large performance drop.
- **Search range**: {`keep_all`, `greedy`}
- **Sensitivity**: high — switching to greedy drops SWE-bench from 50.0% to 39.7%; removing open-ended (effectively more extreme greedy) drops to 23.0%
- **Source**: `DGM_outer.py` argparse; Appendix C.1; ablation results (Table 1)

## sigmoid_lambda (λ)
- **Value**: 10
- **Rationale**: Controls sharpness of sigmoid transform in parent selection. λ=10 provides moderate selection pressure; combined with α₀=0.5 biases toward mid-range performers.
- **Search range**: Not specified in paper
- **Sensitivity**: medium — higher λ approaches greedy argmax; lower λ approaches uniform
- **Source**: Appendix C.2, Equations 3

## sigmoid_alpha0 (α₀)
- **Value**: 0.5
- **Rationale**: Sigmoid midpoint; performance below 50% gets reduced weight. Assumes useful selection range is centered at 50% task solve rate.
- **Search range**: Not specified in paper
- **Sensitivity**: medium — lower α₀ biases toward lower-performing parents; higher α₀ toward higher
- **Source**: Appendix C.2, Equations 3

## quick_eval_task_count
- **Value**: 60
- **Rationale**: Subset used for quick evaluation gate before full eval. Chosen to balance noise reduction (too few = high variance) vs compute cost (too many = not faster than full eval).
- **Search range**: Not specified in paper
- **Sensitivity**: medium — smaller subsets increase noise and may misrank agents; larger subsets increase cost
- **Source**: Appendix A.1, A.2; repo harness configs

## full_eval_task_count
- **Value**: 200
- **Rationale**: Full evaluation subset of SWE-bench Verified (200 tasks) or Polyglot (200 tasks). Used for archive scoring and final benchmark reporting.
- **Search range**: Not specified in paper
- **Sensitivity**: low (correctness boundary) — must be large enough to reliably rank agents
- **Source**: Appendix A.1, A.2

## eval_timeout
- **Value**: 9 hours per agent evaluation
- **Rationale**: Generous timeout to accommodate the longest SWE-bench tasks (complex repo-level fixes). Prevents indefinitely blocking evaluation workers.
- **Search range**: Not specified in paper
- **Sensitivity**: low — most evaluations complete much faster; only edge cases hit this limit
- **Source**: Appendix A.1; repo `swe_bench/harness.py`
