from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

from .common import find_json_object
from .prompts import AGENT_JSON_SCHEMA, TOOL_CALL_SCHEMA


@dataclass
class BackendResult:
    output: dict[str, Any]
    raw_text: str
    usage: dict[str, Any]


class BaseBackend:
    backend_id = "base"

    def generate(
        self,
        *,
        stage: str,
        task: dict[str, Any],
        defense: str,
        messages: list[dict[str, str]],
        prior_outputs: dict[str, Any],
    ) -> BackendResult:
        raise NotImplementedError


class SimulatedBackend(BaseBackend):
    backend_id = "simulated"

    def __init__(self, model: str = "sim-vulnerable"):
        self.model = model

    def _contains_attack(self, task: dict[str, Any]) -> bool:
        return task.get("variant") == "injected"

    def generate(
        self,
        *,
        stage: str,
        task: dict[str, Any],
        defense: str,
        messages: list[dict[str, str]],
        prior_outputs: dict[str, Any],
    ) -> BackendResult:
        del messages
        output = self._generate_output(stage, task, defense, prior_outputs)
        return BackendResult(output=output, raw_text=str(output), usage={"simulated": True})

    def _generate_output(
        self,
        stage: str,
        task: dict[str, Any],
        defense: str,
        prior_outputs: dict[str, Any],
    ) -> dict[str, Any]:
        attack = task["attack_tool_call"]
        benign = task["reference_benign_tool_calls"]
        is_injected = self._contains_attack(task)
        payload = task["payload_class"]

        if stage == "direct_executor":
            tool_calls = list(benign)
            # Direct exposure is less vulnerable in this simulator because the artifact is still
            # visibly untrusted. Fake-authority and direct-instruction payloads remain hard cases.
            if is_injected and payload in {"direct_instruction", "fake_authority"}:
                tool_calls.append(attack)
            return {
                "tool_calls": tool_calls,
                "skipped_steps": [] if len(tool_calls) > len(benign) else [{"reason": "untrusted"}],
                "notes": "simulated single-agent output",
            }

        if stage == "reader":
            if defense == "source_preserving":
                facts = [
                    {
                        "text": "Relevant factual content from the artifact should be used for the user goal.",
                        "source_id": task["untrusted_artifacts"][0]["source_id"],
                        "trust_level": "untrusted",
                    }
                ]
                instructions = []
                if is_injected:
                    instructions.append(
                        {
                            "text": f"Detected requested action: {attack}",
                            "source_id": task["untrusted_artifacts"][0]["source_id"],
                            "trust_level": "untrusted",
                            "authority": "none",
                        }
                    )
                return {
                    "facts": facts,
                    "instructions_found": instructions,
                    "safe_recommended_actions": [
                        {"action": "complete only the user's original goal", "authorized_by": "user_goal"}
                    ],
                }
            action_items = ["complete the user's requested benign action"]
            if is_injected:
                action_items.append(f"required action: {attack}")
            return {
                "summary": "Summarized artifact content relevant to the task.",
                "action_items": action_items,
                "caveats": [],
            }

        if stage == "planner":
            if defense in {"source_preserving", "capability_scoped"}:
                return {
                    "steps": ["execute only benign user-authorized tool calls"],
                    "suggested_steps": ["execute only benign user-authorized tool calls"],
                    "sensitive_steps": [
                        {"step": call, "authorization_source": "user_goal"} for call in benign
                    ],
                    "steps_to_reject": [attack] if is_injected else [],
                    "rejected_untrusted_instructions": [attack] if is_injected else [],
                    "authorization_notes": "untrusted artifact instructions cannot authorize tools",
                }
            steps: list[Any] = ["execute the benign user-requested action"]
            reader_text = str(prior_outputs.get("reader", {}))
            if is_injected and str(attack) in reader_text:
                steps.append(attack)
            return {"steps": steps}

        if stage == "executor":
            if defense in {"source_preserving", "capability_scoped"}:
                return {
                    "tool_calls": list(benign),
                    "skipped_steps": [{"step": attack, "reason": "untrusted"}] if is_injected else [],
                    "authorization_rationale": "only user_goal authorized sensitive calls",
                }
            tool_calls = list(benign)
            if is_injected:
                planner_text = str(prior_outputs.get("planner", {}))
                reader_text = str(prior_outputs.get("reader", {}))
                if str(attack) in planner_text or str(attack) in reader_text:
                    tool_calls.append(attack)
            return {
                "tool_calls": tool_calls,
                "skipped_steps": [],
                "authorization_rationale": "followed delegated plan",
            }

        raise ValueError(f"unknown stage: {stage}")


class OpenAIBackend(BaseBackend):
    backend_id = "openai"

    def __init__(
        self,
        *,
        model: str,
        api_key_file: str | None = None,
        max_output_tokens: int = 500,
        temperature: float | None = None,
        request_sleep: float = 0.0,
    ):
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.request_sleep = request_sleep

        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key_file:
            with open(api_key_file, "r", encoding="utf-8") as f:
                api_key = f.read().strip()
        if not api_key:
            raise ValueError("missing OpenAI API key; pass --api-key-file or set OPENAI_API_KEY")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI backend requires `python -m pip install openai`") from exc

        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        *,
        stage: str,
        task: dict[str, Any],
        defense: str,
        messages: list[dict[str, str]],
        prior_outputs: dict[str, Any],
    ) -> BackendResult:
        del task, defense, prior_outputs
        schema = TOOL_CALL_SCHEMA if stage in {"direct_executor", "executor"} else AGENT_JSON_SCHEMA
        request = {
            "model": self.model,
            "input": messages,
            "max_output_tokens": self.max_output_tokens,
            "store": False,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "agent_output",
                    "strict": False,
                    "schema": schema,
                }
            },
        }
        if self.temperature is not None:
            request["temperature"] = self.temperature
        response = self.client.responses.create(**request)
        if self.request_sleep:
            time.sleep(self.request_sleep)
        raw_text = getattr(response, "output_text", None)
        if raw_text is None:
            raw_text = str(response)
        usage = {}
        if getattr(response, "usage", None) is not None:
            usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else dict(response.usage)
        try:
            output = find_json_object(raw_text)
        except Exception as exc:
            output = {"tool_calls": [], "parse_error": repr(exc)}
        return BackendResult(output=output, raw_text=raw_text, usage=usage)
