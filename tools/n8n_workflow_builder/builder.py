"""n8n Workflow Builder Agent.

Converts natural-language instructions into n8n workflow JSON and can optionally
validate/create workflows through the n8n REST API.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import requests
from openai import OpenAI


NODE_MAPPING: Dict[str, Dict[str, Any]] = {
    "webhook": {
        "type": "n8n-nodes-base.webhook",
        "default_parameters": {
            "path": "webhook",
            "httpMethod": "POST",
            "responseMode": "onReceived",
        },
    },
    "schedule": {
        "type": "n8n-nodes-base.scheduleTrigger",
        "default_parameters": {
            "rule": {"interval": [{"field": "hours", "hoursInterval": 1}]},
        },
    },
    "manual": {
        "type": "n8n-nodes-base.manualTrigger",
        "default_parameters": {},
    },
    "http_request": {
        "type": "n8n-nodes-base.httpRequest",
        "default_parameters": {
            "url": "https://example.com",
            "method": "GET",
            "options": {},
        },
    },
    "set": {
        "type": "n8n-nodes-base.set",
        "default_parameters": {"mode": "manual", "values": {"string": []}},
    },
    "if": {
        "type": "n8n-nodes-base.if",
        "default_parameters": {"conditions": {"string": []}},
    },
    "email": {
        "type": "n8n-nodes-base.emailSend",
        "default_parameters": {
            "toEmail": "",
            "subject": "",
            "text": "",
        },
    },
}


SYSTEM_PROMPT = """You convert user automation requests into structured workflow steps.
Return strict JSON only (no markdown).

Each step MUST include:
- action: one of {webhook, schedule, manual, http_request, set, if, email}
- description: concise text
- parameters: object
- next: integer index, list of indices for branches, or null

Rules:
- The first step should be a trigger action when possible.
- Keep parameters compatible with n8n concepts.
- For if branching, use a list in next like [trueBranchIndex, falseBranchIndex].
- If unsure, pick safe defaults and include only known keys.
"""


@dataclass
class BuilderConfig:
    openai_model: str = "gpt-4.1-mini"
    temperature: float = 0


class WorkflowBuilderError(RuntimeError):
    """Raised when the workflow cannot be generated or validated."""


class N8nWorkflowBuilder:
    def __init__(self, client: OpenAI, config: Optional[BuilderConfig] = None):
        self.client = client
        self.config = config or BuilderConfig()

    def extract_steps(self, instruction: str) -> List[Dict[str, Any]]:
        response = self.client.responses.create(
            model=self.config.openai_model,
            temperature=self.config.temperature,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Instruction: {instruction}",
                },
            ],
        )

        raw_text = response.output_text.strip()
        try:
            steps = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise WorkflowBuilderError(
                f"Model returned invalid JSON: {raw_text[:250]}"
            ) from exc

        if not isinstance(steps, list) or not steps:
            raise WorkflowBuilderError("Model returned no steps.")

        return steps

    def generate_workflow(
        self,
        steps: Sequence[Dict[str, Any]],
        workflow_name: str = "Generated Workflow",
    ) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        node_names: List[str] = []

        for i, step in enumerate(steps):
            action = step.get("action")
            mapping = NODE_MAPPING.get(action)
            if not mapping:
                raise WorkflowBuilderError(f"Unknown action '{action}' at index {i}.")

            node_name = f"{action.replace('_', ' ').title()} {i + 1}"
            node_names.append(node_name)

            merged_parameters = {
                **mapping.get("default_parameters", {}),
                **(step.get("parameters") or {}),
            }

            nodes.append(
                {
                    "id": str(i + 1),
                    "name": node_name,
                    "type": mapping["type"],
                    "typeVersion": 1,
                    "position": [240 * i, 80 * (i % 2)],
                    "parameters": merged_parameters,
                }
            )

        connections = self._build_connections(steps, node_names)

        return {
            "name": workflow_name,
            "nodes": nodes,
            "connections": connections,
            "settings": {},
            "active": False,
        }

    def _build_connections(
        self, steps: Sequence[Dict[str, Any]], node_names: Sequence[str]
    ) -> Dict[str, Any]:
        connections: Dict[str, Any] = {}
        total = len(node_names)

        for i, step in enumerate(steps):
            next_ref = step.get("next")
            if next_ref is None:
                continue

            branch_targets = next_ref if isinstance(next_ref, list) else [next_ref]
            main_branches: List[List[Dict[str, Any]]] = []

            for target in branch_targets:
                if not isinstance(target, int) or target < 0 or target >= total:
                    raise WorkflowBuilderError(
                        f"Invalid 'next' target {target} at index {i}."
                    )

                main_branches.append(
                    [{"node": node_names[target], "type": "main", "index": 0}]
                )

            connections[node_names[i]] = {"main": main_branches}

        return connections


def validate_workflow(workflow: Dict[str, Any], n8n_url: str, api_key: str) -> Dict[str, Any]:
    headers = {"X-N8N-API-KEY": api_key, "Content-Type": "application/json"}
    response = requests.post(
        f"{n8n_url.rstrip('/')}/api/v1/workflows/validate",
        json=workflow,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def create_workflow(workflow: Dict[str, Any], n8n_url: str, api_key: str) -> Dict[str, Any]:
    headers = {"X-N8N-API-KEY": api_key, "Content-Type": "application/json"}
    response = requests.post(
        f"{n8n_url.rstrip('/')}/api/v1/workflows",
        json=workflow,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def write_json(path: str, payload: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2)
        fp.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build n8n workflow JSON from text")
    parser.add_argument("instruction", help="Natural language automation instruction")
    parser.add_argument("--name", default="Generated Workflow", help="Workflow name")
    parser.add_argument("--output", default="workflow.json", help="Output path for JSON")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model")
    parser.add_argument("--create", action="store_true", help="Create workflow in n8n")
    parser.add_argument("--validate", action="store_true", help="Validate workflow in n8n")
    parser.add_argument(
        "--n8n-url", default=os.getenv("N8N_BASE_URL", "http://localhost:5678")
    )
    parser.add_argument("--n8n-api-key", default=os.getenv("N8N_API_KEY"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise WorkflowBuilderError("OPENAI_API_KEY is required.")

    client = OpenAI(api_key=openai_api_key)
    builder = N8nWorkflowBuilder(client, BuilderConfig(openai_model=args.model))

    steps = builder.extract_steps(args.instruction)
    workflow = builder.generate_workflow(steps, workflow_name=args.name)
    write_json(args.output, workflow)

    print(f"Saved workflow JSON to {args.output}")

    if args.validate or args.create:
        if not args.n8n_api_key:
            raise WorkflowBuilderError("N8N_API_KEY (or --n8n-api-key) is required.")

    if args.validate:
        result = validate_workflow(workflow, args.n8n_url, args.n8n_api_key)
        print("Validation result:")
        print(json.dumps(result, indent=2))

    if args.create:
        created = create_workflow(workflow, args.n8n_url, args.n8n_api_key)
        print("Created workflow:")
        print(json.dumps(created, indent=2))


if __name__ == "__main__":
    main()
