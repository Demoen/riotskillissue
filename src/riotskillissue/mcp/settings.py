"""Environment-backed settings for the local MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Mapping

from .errors import McpConfigurationError

DEFAULT_INLINE_LIMIT = 32 * 1024
DEFAULT_MAX_RESULTS = 64
DEFAULT_RESULT_TTL = 600.0
DEFAULT_MAX_RESULT_SIZE = 10 * 1024 * 1024


@dataclass(frozen=True)
class RiotMcpSettings:
    """Validated settings used by one MCP server lifespan."""

    api_key: str = field(repr=False)
    default_route: str | None = None
    allow_writes: bool = False
    inline_limit: int = DEFAULT_INLINE_LIMIT
    max_results: int = DEFAULT_MAX_RESULTS
    result_ttl: float = DEFAULT_RESULT_TTL
    max_result_size: int = DEFAULT_MAX_RESULT_SIZE

    def __post_init__(self) -> None:
        if not self.api_key.strip():
            raise McpConfigurationError(
                "RIOT_API_KEY is required to start the RiotSkillIssue MCP server."
            )
        if self.inline_limit < 1:
            raise McpConfigurationError("The MCP inline result limit must be positive.")
        if self.max_results < 1:
            raise McpConfigurationError("The MCP result capacity must be positive.")
        if self.result_ttl <= 0:
            raise McpConfigurationError("The MCP result TTL must be positive.")
        if self.max_result_size < self.inline_limit:
            raise McpConfigurationError(
                "The MCP result size ceiling cannot be smaller than the inline limit."
            )

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "RiotMcpSettings":
        """Load credentials and server policy from environment variables."""
        values = os.environ if environ is None else environ
        api_key = values.get("RIOT_API_KEY", "").strip()
        route = (
            values.get("RIOT_MCP_DEFAULT_ROUTE")
            or values.get("RIOT_DEFAULT_ROUTE")
            or ""
        ).strip()
        allow_writes = _parse_bool(
            values.get("RIOT_MCP_ALLOW_WRITES", "false"),
            "RIOT_MCP_ALLOW_WRITES",
        )
        return cls(
            api_key=api_key,
            default_route=route or None,
            allow_writes=allow_writes,
        )


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off", ""}:
        return False
    raise McpConfigurationError(f"{name} must be a boolean value.")
