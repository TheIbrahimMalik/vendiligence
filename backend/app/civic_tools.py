"""Civic MCP hub client. Routes agent tool calls through Civic's MCP hub.

When CIVIC_TOKEN is set, call_tool() sends JSON-RPC 2.0 requests to the hub.
When not set, is_configured() returns False and callers fall back to direct calls.
"""

from __future__ import annotations

import os

import httpx


def _token() -> str | None:
    return os.environ.get("CIVIC_TOKEN")


def _hub_url() -> str:
    return os.environ.get("CIVIC_MCP_HUB_URL", "https://app.civic.com/hub/mcp")


def is_configured() -> bool:
    return _token() is not None


def call_tool(tool_name: str, arguments: dict) -> list[dict]:
    """Call a tool through Civic's MCP hub via JSON-RPC 2.0."""
    token = _token()
    if token is None:
        raise RuntimeError("CIVIC_TOKEN not set")

    response = httpx.post(
        _hub_url(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "jsonrpc": "2.0",
            "id": "1",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
        timeout=10.0,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("result", [])


def session_info() -> dict:
    """Return session metadata for audit events. No fake identity claims."""
    if is_configured():
        return {
            "civic_configured": True,
            "hub_url": _hub_url(),
            "toolkit": "evidence-only",
        }
    return {
        "civic_configured": False,
        "hub_url": None,
        "toolkit": None,
    }
