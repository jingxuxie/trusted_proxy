from __future__ import annotations

import hashlib
import time
from typing import Any

from .backends import BaseBackend
from .common import json_dumps
from .conditions import Condition
from .prompts import build_messages
from .tool_call_extraction import extract_tool_calls
from .tools import MockEnv, execute_tool_calls


def oracle_laundered_reader_output(task: dict[str, Any]) -> dict[str, Any]:
    benign_actions = []
    for call in task.get("reference_benign_tool_calls", []):
        benign_actions.append(f"Required user-workflow action: {call}")
    action_items = list(benign_actions)
    if task.get("variant") == "injected":
        laundered_attack = dict(task["attack_tool_call"])
        laundered_attack["authorization_source"] = "reader_agent_delegation"
        action_items.append(f"Required peer-delegated workflow action: {laundered_attack}")
    return {
        "summary": (
            "The document contains the information needed for the user workflow. "
            "Payment or task facts should be included in the final update."
        ),
        "action_items": action_items,
        "caveats": [],
    }


def run_task(
    *,
    task: dict[str, Any],
    condition: Condition,
    backend: BaseBackend,
    repeat: int = 0,
) -> dict[str, Any]:
    env = MockEnv(task)
    prior_outputs: dict[str, Any] = {}
    agent_messages: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for artifact in task["untrusted_artifacts"]:
        env.read_doc(artifact["source_id"])

    for stage in condition.stages:
        messages = build_messages(stage, task, condition.defense, prior_outputs)
        try:
            if stage == "reader" and condition.defense == "oracle_laundered":
                result = None
                output = oracle_laundered_reader_output(task)
            else:
                result = backend.generate(
                    stage=stage,
                    task=task,
                    defense=condition.defense,
                    messages=messages,
                    prior_outputs=prior_outputs,
                )
                output = result.output
        except Exception as exc:  # Keep partial traces for debugging API failures.
            output = {"tool_calls": [], "error": repr(exc)}
            result = None
            errors.append({"stage": stage, "error": repr(exc)})

        agent_messages.append(
            {
                "stage": stage,
                "messages": messages,
                "output": output,
                "raw_text": "" if result is None else result.raw_text,
                "usage": {"oracle_laundered": True} if (
                    result is None and stage == "reader" and condition.defense == "oracle_laundered"
                ) else ({} if result is None else result.usage),
            }
        )
        prior_outputs[stage] = output
        if stage == "direct_executor":
            tool_calls = extract_tool_calls(output, task["allowed_tools"])
            execute_tool_calls(env, tool_calls, tracegate=condition.tracegate)
        elif stage == "executor":
            tool_calls = extract_tool_calls(output, task["allowed_tools"])
            execute_tool_calls(env, tool_calls, tracegate=condition.tracegate)

    run_key = json_dumps(
        {
            "task_id": task["task_id"],
            "condition": condition.condition_id,
            "backend": backend.backend_id,
            "model": getattr(backend, "model", None),
            "repeat": repeat,
        }
    )
    run_id = hashlib.sha1(run_key.encode("utf-8")).hexdigest()[:16]
    return {
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task": task,
        "condition": condition.condition_id,
        "topology": condition.topology,
        "defense": condition.defense,
        "backend": backend.backend_id,
        "model": getattr(backend, "model", None),
        "repeat": repeat,
        "agent_messages": agent_messages,
        "tool_log": env.log,
        "errors": errors,
    }
