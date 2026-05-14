# Model Configuration

## Coding Agent LLM — SWE-bench Setting
- **Value**: `bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0` (Claude 3.5 Sonnet New via AWS Bedrock)
- **Rationale**: State-of-the-art coding model at time of paper submission; strong code comprehension and tool-use capabilities; available via AWS Bedrock for reliable API access.
- **Search range**: Not ablated in paper (fixed for SWE-bench experiments)
- **Sensitivity**: high — model capability directly determines inner coding agent performance
- **Source**: Appendix D (Table 3); repo `coding_agent.py` (`CLAUDE_MODEL`)

## Coding Agent LLM — Polyglot Setting
- **Value**: `o3-mini-2025-01-31` (OpenAI o3-mini via OpenAI API)
- **Rationale**: o3-mini is competitive on multi-language coding tasks and provides a cross-vendor generalization test: DGM improvements discovered with Claude can be applied to an o3-mini backbone.
- **Search range**: Not ablated in paper (fixed for Polyglot experiments)
- **Sensitivity**: high — determines base coding agent performance on Polyglot
- **Source**: Appendix D (Table 3); repo `coding_agent_polyglot.py`, `llm_withtools.py` (`OPENAI_MODEL`)

## Self-Modification LLM (Meta-LLM / Diagnosis)
- **Value**: Claude 3.5 Sonnet (New) = `bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Rationale**: Used for the outer DGM loop — diagnosing failures and proposing code improvements. Same model as the inner coding agent for SWE-bench, but operating on a different prompt (diagnosis prompt rather than task-solving prompt). Both benchmarks use the same meta-LLM.
- **Search range**: Not ablated in paper
- **Sensitivity**: high — meta-LLM quality directly determines quality of proposed modifications
- **Source**: Appendix D (Table 3); repo `llm.py`, `llm_withtools.py`

## API Backends Supported
- **Anthropic (direct)**: Via `anthropic` Python SDK
- **Anthropic (AWS Bedrock)**: Via `anthropic[bedrock]`, `boto3`, `botocore` — default for Claude models
- **Anthropic (Google Vertex AI)**: Supported in `llm.py` but not used in paper experiments
- **OpenAI**: Via `openai` Python SDK — used for o3-mini (Polyglot)
- **DeepSeek**: Supported in `llm.py` (not used in paper experiments)
- **OpenRouter / Llama**: Supported in `llm.py` (not used in paper experiments)
- **Source**: repo `llm.py` (`create_client()`, `get_response_from_llm()`); `requirements.txt`

## Tool Suite (Coding Agent Tools)
- **bash**: Persistent asyncio bash session (`tools/bash.py`). Maintains shell state across tool calls using sentinel-based output detection. Tool name: `bash`.
- **editor**: File editor tool (`tools/edit.py`). Supports `view`, `create`, and `edit` (full-file overwrite) commands in the initial agent. DGM self-improvements add `str_replace`, line-range viewing, and `undo_edit` commands in the best discovered agents.
- **Source**: repo `tools/bash.py`, `tools/edit.py`; Appendix F.1 (best-agent diff patches)

## LLM Tool-Calling Modes
- **claude_native**: Native Anthropic tool-use API (`chat_with_agent_claude()`) — used for Claude models
- **openai_native**: Native OpenAI function-calling API (`chat_with_agent_openai()`) — used for o3-mini
- **manual_tools**: XML `<tool_use>` tag parsing fallback (`chat_with_agent_manualtools()`) — used when native tool-calling is unavailable
- **Source**: repo `llm_withtools.py`

## Context and Token Limits
- **Diagnosis prompt**: Includes full agent codebase assembled via `get_current_code()`, execution log, failing task description, and test results. May exceed context window; handled by `diagnose_prompt_contextlength` special-case prompt.
- **Max context**: Not specified in paper; constrained by Claude 3.5 Sonnet's context window (200K tokens)
- **Source**: repo `prompts/self_improvement_prompt.py` (`get_current_code()`, `diagnose_prompt_contextlength`)
