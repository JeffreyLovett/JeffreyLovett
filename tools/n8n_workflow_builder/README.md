# n8n Workflow Builder Agent

This module turns natural language instructions into n8n workflow JSON using OpenAI, then optionally validates or creates the workflow via the n8n REST API.

## Features

- Converts text instructions into structured workflow steps with an LLM.
- Maps extracted steps to n8n node types and auto-builds connections.
- Writes ready-to-import workflow JSON to disk.
- Optional API calls to validate and create workflows in n8n.

## Requirements

```bash
pip install openai requests
```

Environment variables:

- `OPENAI_API_KEY` (required)
- `N8N_API_KEY` (required for `--validate` and `--create`)
- `N8N_BASE_URL` (optional, defaults to `http://localhost:5678`)

## Usage

Generate JSON only:

```bash
python tools/n8n_workflow_builder/builder.py \
  "When a webhook is called on /update, fetch https://api.example.com/data and email the response" \
  --name "Webhook Fetch + Email" \
  --output workflow.json
```

Generate and validate in n8n:

```bash
python tools/n8n_workflow_builder/builder.py \
  "Run every hour and GET https://api.example.com/health" \
  --validate
```

Generate and create in n8n:

```bash
python tools/n8n_workflow_builder/builder.py \
  "Manual trigger then POST JSON to https://api.example.com/submit" \
  --create
```

## Notes

- `next` can be a single index (`2`) for linear flow or a list (`[3, 4]`) for branches.
- If the LLM returns unknown actions or bad indices, the script raises `WorkflowBuilderError`.
- Extend `NODE_MAPPING` in `builder.py` to support more n8n nodes.
