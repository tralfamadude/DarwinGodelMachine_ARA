# Table 3 — Foundation Models Used Per Experiment Setting

**Source**: Table 3 in "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents" (arXiv:2505.22954)
**Caption**: Foundation models used for self-modification (meta-LLM / outer loop) and evaluation (inner coding agent) in each benchmark setting.
**Extraction type**: raw_table
**Section**: Appendix D.1

| Benchmark | Self-Modification LLM | Evaluation / Coding Agent LLM |
|-----------|----------------------|-------------------------------|
| SWE-bench | Claude 3.5 Sonnet (New) | Claude 3.5 Sonnet (New) |
| Polyglot | Claude 3.5 Sonnet (New) | o3-mini |

**Notes**:
- "Self-Modification LLM" = the meta-LLM used in the outer DGM loop for diagnosing failing tasks and proposing code modifications (diagnosis prompt in `prompts/self_improvement_prompt.py`)
- "Evaluation / Coding Agent LLM" = the model used inside the inner coding agent to solve benchmark tasks
- Claude 3.5 Sonnet (New) model ID: `bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0` (from repo `coding_agent.py`, `llm_withtools.py`)
- o3-mini model ID: `o3-mini-2025-01-31` (from repo `llm_withtools.py`)
- Using o3-mini for Polyglot evaluation enables a cross-model generalization test: DGM improvements discovered via Claude-based self-modification are validated on an o3-mini backbone
