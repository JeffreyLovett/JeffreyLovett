# Integration

Guidelines for integrating third-party APIs such as OpenAI, Meetup, Eventbrite, Pixlr, and Canva.

- Configure API keys in the `.env` file.
- Implement service wrappers in `src/services` for each provider.
- Use these services throughout the app to fetch data and perform actions.

## n8n Workflow Builder Agent

The repository includes a Python-based workflow generator at `tools/n8n_workflow_builder/builder.py`.
It uses OpenAI to convert natural language instructions into n8n workflow JSON and can optionally call n8n API endpoints to validate or create workflows.
