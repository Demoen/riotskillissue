"""Optional local MCP server support."""

from __future__ import annotations

from typing import Any

from .errors import McpConfigurationError
from .result_store import ResultStore
from .settings import RiotMcpSettings

__all__ = [
    "ResultStore",
    "RiotMcpSettings",
    "create_server",
    "main",
]


def create_server(*args: Any, **kwargs: Any) -> Any:
    """Create the stdio MCP server.

    The MCP SDK is imported only when this function is called.
    """
    try:
        from .server import create_server as _create_server
    except (ImportError, ModuleNotFoundError) as exc:
        if exc.name == "mcp" or (exc.name or "").startswith("mcp."):
            raise McpConfigurationError(
                "MCP support is not installed. Install riotskillissue with the mcp extra."
            ) from None
        if exc.name == "mcp_types" or (exc.name or "").startswith("mcp_types."):
            raise McpConfigurationError(
                "MCP support is incomplete. Reinstall riotskillissue with the mcp extra."
            ) from None
        raise
    return _create_server(*args, **kwargs)


def main() -> None:
    """Run the local stdio MCP server."""
    create_server().run(transport="stdio")
