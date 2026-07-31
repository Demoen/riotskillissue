"""Safe errors for the MCP boundary."""

from __future__ import annotations

import re
from typing import Any

_SECRET_KEYS = {
    "access_token",
    "api_key",
    "apikey",
    "authorization",
    "client_secret",
    "credential",
    "password",
    "refresh_token",
    "riot_token",
    "secret",
    "token",
}
_SECRET_VALUE_PATTERNS = (
    re.compile(r"RGAPI-[A-Za-z0-9_-]+", re.IGNORECASE),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    re.compile(
        r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"
    ),
)


class RiotMcpError(Exception):
    """Base class for errors safe to return through MCP."""


class McpConfigurationError(RiotMcpError):
    """The local server configuration is invalid."""


class McpSecurityError(RiotMcpError):
    """A request violates an MCP security boundary."""


class OperationNotFoundError(RiotMcpError):
    """The requested public operation does not exist."""


class OperationNotAllowedError(McpSecurityError):
    """The requested operation is not exposed by this server."""


class InvalidArgumentsError(RiotMcpError):
    """Tool arguments are invalid."""


class ResultNotFoundError(RiotMcpError):
    """A retained result is missing or expired."""


class InvalidPointerError(RiotMcpError):
    """A JSON Pointer cannot be resolved."""


class ResultTooLargeError(RiotMcpError):
    """A result exceeds the in-memory retention ceiling."""


class ResultEncodingError(RiotMcpError):
    """A result cannot be represented as JSON."""


class IntegrationContractError(RiotMcpError):
    """The installed RiotSkillIssue API does not meet the MCP contract."""


def is_sensitive_key(key: object) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")
    if normalized in _SECRET_KEYS:
        return True
    if normalized.endswith(
        ("_access_token", "_api_key", "_refresh_token", "_riot_token")
    ):
        return True
    segments = set(normalized.split("_"))
    return bool(
        segments.intersection(
            {"authorization", "credential", "password", "secret"}
        )
    )


def redact_text(value: str) -> str:
    redacted = value
    for pattern in _SECRET_VALUE_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def contains_secret_value(value: str) -> bool:
    return any(pattern.search(value) is not None for pattern in _SECRET_VALUE_PATTERNS)


def sanitize_exception(exc: Exception) -> RiotMcpError:
    if isinstance(exc, RiotMcpError):
        return exc
    if isinstance(exc, (TypeError, ValueError)):
        return InvalidArgumentsError("The operation arguments are invalid.")

    name = type(exc).__name__.lower()
    if "ratelimit" in name or "rate_limit" in name:
        return RiotMcpError("The Riot API rate limit was exhausted. Try again later.")
    if "timeout" in name:
        return RiotMcpError("The Riot API request timed out. Try again.")
    if "route" in name:
        return InvalidArgumentsError(
            "The route could not be resolved. Provide a supported route for this operation."
        )
    if "credential" in name or "authentication" in name or "unauthorized" in name:
        return McpConfigurationError("The server's Riot API credentials were rejected.")
    if "validation" in name or "malformed" in name or "decode" in name:
        return RiotMcpError("Riot returned an invalid response for this operation.")
    if "network" in name or "connect" in name or "http" in name:
        return RiotMcpError("The Riot API could not be reached. Try again.")

    status = _status_code(exc)
    if status == 404:
        return RiotMcpError("The requested Riot resource was not found.")
    if status == 403:
        return RiotMcpError("The Riot API denied access to this resource.")
    if status == 429:
        return RiotMcpError("The Riot API rate limit was exhausted. Try again later.")
    if status is not None and 400 <= status < 500:
        return InvalidArgumentsError("Riot rejected the operation arguments.")
    if status is not None and status >= 500:
        return RiotMcpError("The Riot API is temporarily unavailable.")

    return RiotMcpError("The Riot API operation failed.")


def _status_code(exc: Exception) -> int | None:
    status = getattr(exc, "status_code", None)
    if not isinstance(status, int):
        status = getattr(exc, "status", None)
    if isinstance(status, int):
        return status

    response: Any = getattr(exc, "response", None)
    response_status = getattr(response, "status_code", None)
    return response_status if isinstance(response_status, int) else None
