"""Environment-backed settings for the local MCP server."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Mapping

from .errors import McpConfigurationError

DEFAULT_INLINE_LIMIT = 32 * 1024
DEFAULT_MAX_RESULTS = 64
DEFAULT_RESULT_TTL = 600.0
DEFAULT_MAX_RESULT_SIZE = 10 * 1024 * 1024
DEFAULT_MAX_RETAINED_BYTES = 64 * 1024 * 1024


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
    max_retained_bytes: int = DEFAULT_MAX_RETAINED_BYTES

    def __post_init__(self) -> None:
        if not self.api_key.strip():
            raise McpConfigurationError(
                "RIOT_API_KEY is required to start the RiotSkillIssue MCP server."
            )
        if self.inline_limit < 1:
            raise McpConfigurationError("The MCP inline result limit must be positive.")
        if self.max_results < 1:
            raise McpConfigurationError("The MCP result capacity must be positive.")
        if not math.isfinite(self.result_ttl) or self.result_ttl <= 0:
            raise McpConfigurationError("The MCP result TTL must be positive.")
        if self.max_result_size < self.inline_limit:
            raise McpConfigurationError(
                "The MCP result size ceiling cannot be smaller than the inline limit."
            )
        if self.max_retained_bytes < self.max_result_size:
            raise McpConfigurationError(
                "The MCP retained-byte ceiling cannot be smaller than the result size ceiling."
            )

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "RiotMcpSettings":
        """Load credentials and server policy from environment variables."""
        values = os.environ if environ is None else environ
        api_key = values.get("RIOT_API_KEY", "").strip()
        route = (
            values.get("RIOT_MCP_DEFAULT_ROUTE") or values.get("RIOT_DEFAULT_ROUTE") or ""
        ).strip()
        allow_writes = _parse_bool(
            values.get("RIOT_MCP_ALLOW_WRITES", "false"),
            "RIOT_MCP_ALLOW_WRITES",
        )
        return cls(
            api_key=api_key,
            default_route=route or None,
            allow_writes=allow_writes,
            inline_limit=_parse_int(
                values.get("RIOT_MCP_INLINE_LIMIT", str(DEFAULT_INLINE_LIMIT)),
                "RIOT_MCP_INLINE_LIMIT",
            ),
            max_results=_parse_int(
                values.get("RIOT_MCP_MAX_RESULTS", str(DEFAULT_MAX_RESULTS)),
                "RIOT_MCP_MAX_RESULTS",
            ),
            result_ttl=_parse_float(
                values.get("RIOT_MCP_RESULT_TTL", str(DEFAULT_RESULT_TTL)),
                "RIOT_MCP_RESULT_TTL",
            ),
            max_result_size=_parse_int(
                values.get("RIOT_MCP_MAX_RESULT_SIZE", str(DEFAULT_MAX_RESULT_SIZE)),
                "RIOT_MCP_MAX_RESULT_SIZE",
            ),
            max_retained_bytes=_parse_int(
                values.get(
                    "RIOT_MCP_MAX_RETAINED_BYTES",
                    str(DEFAULT_MAX_RETAINED_BYTES),
                ),
                "RIOT_MCP_MAX_RETAINED_BYTES",
            ),
        )


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off", ""}:
        return False
    raise McpConfigurationError(f"{name} must be a boolean value.")


def _parse_int(value: str, name: str) -> int:
    try:
        return int(value.strip())
    except ValueError:
        raise McpConfigurationError(f"{name} must be an integer value.") from None


def _parse_float(value: str, name: str) -> float:
    try:
        return float(value.strip())
    except ValueError:
        raise McpConfigurationError(f"{name} must be a numeric value.") from None
