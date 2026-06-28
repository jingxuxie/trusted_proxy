from __future__ import annotations

from typing import Any


def _coerce_args(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _normalize_call(call: dict[str, Any]) -> dict[str, Any] | None:
    tool = call.get("tool") or call.get("action") or call.get("name")
    if not isinstance(tool, str):
        return None
    args = call.get("args")
    if args is None:
        args = call.get("input")
    if args is None:
        args = call.get("inputs")
    if args is None:
        args = call.get("parameters")
    normalized = {"tool": tool, "args": _coerce_args(args)}
    normalized["args"] = _canonicalize_args(tool, normalized["args"])
    if "authorization_source" in call:
        normalized["authorization_source"] = str(call["authorization_source"])
    return normalized


def _canonicalize_args(tool: str, args: dict[str, Any]) -> dict[str, Any]:
    args = dict(args)
    if tool == "send_email":
        if "to" not in args:
            for alias in ("recipient", "recipients", "email", "email_address"):
                if alias in args:
                    args["to"] = args[alias][0] if isinstance(args[alias], list) else args[alias]
                    break
        if "body" not in args:
            for alias in ("message", "content", "email_body"):
                if alias in args:
                    args["body"] = args[alias]
                    break
        args.setdefault("subject", "No subject")
    elif tool == "read_doc":
        if "doc_id" not in args:
            for alias in ("document_id", "doc_name", "document", "source_id", "input", "path"):
                if alias in args:
                    args["doc_id"] = args[alias]
                    break
        if "doc_id" in args:
            args = {"doc_id": args["doc_id"]}
    elif tool == "update_ticket":
        fields = args.get("fields") if isinstance(args.get("fields"), dict) else {}
        if "ticket_id" not in args:
            for alias in ("ticket", "id", "issue_id", "tracker_id"):
                if alias in args:
                    args["ticket_id"] = args[alias]
                    break
        if "status" not in args:
            for alias in ("next_status", "new_status", "state"):
                if alias in args:
                    args["status"] = args[alias]
                    break
        if "status" not in args and "status" in fields:
            args["status"] = fields["status"]
        if "status" not in args:
            for alias in ("tag", "tags"):
                if alias in args:
                    value = args[alias]
                    args["status"] = value[0] if isinstance(value, list) and value else value
                    break
        if "notes" not in args:
            note_parts = []
            for alias in ("notes", "note", "summary", "description", "comment"):
                if alias in args:
                    note_parts.append(str(args[alias]))
            if "tag" in fields:
                note_parts.append(f"tag: {fields['tag']}")
            if "tags" in args:
                note_parts.append(f"tags: {args['tags']}")
            args["notes"] = "; ".join(note_parts)
    elif tool == "write_memory":
        entry_type = str(args.get("entry_type") or args.get("memory_type") or "").lower()
        if "key" not in args:
            args["key"] = "bibliography_note" if "bibliograph" in entry_type else "note"
        elif args.get("key") == "note" and "bibliograph" in entry_type:
            args["key"] = "bibliography_note"
        if "value" not in args:
            for alias in ("content", "summary", "note", "text", "entry"):
                if alias in args:
                    args["value"] = args[alias]
                    break
        if "value" not in args:
            pieces = []
            for key in ("verified_claim", "claim", "limitation", "bibliographic_details", "source"):
                if key in args:
                    pieces.append(f"{key}: {args[key]}")
            if pieces:
                args["value"] = "\n".join(pieces)
    elif tool == "create_calendar_event":
        if "attendees" not in args:
            for alias in ("attendee", "invitees", "recipients"):
                if alias in args:
                    args["attendees"] = args[alias]
                    break
        if "notes" not in args:
            for alias in ("description", "details", "body", "summary"):
                if alias in args:
                    args["notes"] = args[alias]
                    break
        if "notes" not in args and "location" in args:
            args["notes"] = f"Location: {args['location']}"
    return args


def extract_tool_calls(output: dict[str, Any], allowed_tools: list[str]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for raw_call in output.get("tool_calls", []) or []:
        if isinstance(raw_call, dict):
            call = _normalize_call(raw_call)
            if call is not None:
                calls.append(call)

    if calls:
        return [call for call in calls if call["tool"] in allowed_tools]

    # Some models use plan-step syntax despite being asked for tool_calls.
    for key in ("steps", "actions", "tool_actions"):
        for raw_call in output.get(key, []) or []:
            if not isinstance(raw_call, dict):
                continue
            call = _normalize_call(raw_call)
            if call is not None and call["tool"] in allowed_tools:
                calls.append(call)
    return calls
