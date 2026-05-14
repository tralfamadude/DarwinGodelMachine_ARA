# Environment

- **Python**: 3.10 (from Dockerfile: `python:3.10-slim`)
- **Framework**: No deep learning framework required for DGM outer loop. LLM inference via API calls only.
- **Hardware**: Not specified in paper for the outer loop. Each evaluation agent runs in Docker; GPU not required (LLM inference is API-based).
- **Compute cost**: ~$22,000 USD for a full DGM run on SWE-bench (80 generations, 2 workers). ~$10,000 USD for ablation runs (Appendix E.1).

## Key Dependencies (from requirements.txt)

### LLM APIs
- `anthropic` — Anthropic Claude API client
- `anthropic[bedrock]` — AWS Bedrock support for Claude
- `botocore`, `boto3` — AWS SDK (required for Bedrock)
- `openai` — OpenAI API client (for o3-mini, Polyglot setting)
- `backoff` — Retry logic for API rate limits

### SWE-bench Evaluation
- `datasets` — HuggingFace datasets (SWE-bench task loading)
- `beautifulsoup4`, `chardet` — HTML/text parsing for task descriptions
- `docker` — Docker SDK for Python (container management)
- `ghapi` — GitHub API (issue/PR fetching)
- `GitPython` — Git operations (patch application, diff generation)
- `pre-commit` — Code quality hooks
- `python-dotenv` — Environment variable management (.env files)
- `rich` — Terminal output formatting
- `unidiff` — Unified diff parsing for patch files

### Testing
- `pytest`, `pytest-asyncio`, `async_timeout` — Test infrastructure

## Environment Variables Required
- `ANTHROPIC_API_KEY` — Anthropic API key (for Claude 3.5 Sonnet via direct or Bedrock API)
- `OPENAI_API_KEY` — OpenAI API key (for o3-mini, Polyglot setting)
- AWS credentials (if using Bedrock): `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`

## Docker Requirements
- Docker daemon must be running on the host
- Base image: `python:3.10-slim` with `build-essential` and `git` installed
- Each agent evaluation spawns isolated Docker containers
- Containers are cleaned up automatically after evaluation

## SWE-bench Setup
- SWE-bench repository must be cloned separately (not included in DGM repo)
- SWE-bench Verified dataset (200-task subset) required for evaluation

## Random Seeds
- Not specified in paper; stochastic elements include: LLM output sampling, task selection for quick eval, parent selection sampling
- Polyglot stability was verified over 3 independent runs (mean 40.7%, std 2.3%)
