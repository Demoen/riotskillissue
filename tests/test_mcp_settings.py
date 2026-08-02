from __future__ import annotations

import pytest

from riotskillissue.mcp.errors import McpConfigurationError
from riotskillissue.mcp.settings import (
    DEFAULT_MAX_RETAINED_BYTES,
    DEFAULT_MAX_RESULT_SIZE,
    RiotMcpSettings,
)


def test_settings_load_all_result_limits_from_environment() -> None:
    settings = RiotMcpSettings.from_env(
        {
            "RIOT_API_KEY": " RGAPI-private ",
            "RIOT_MCP_INLINE_LIMIT": "1024",
            "RIOT_MCP_MAX_RESULTS": "12",
            "RIOT_MCP_RESULT_TTL": "45.5",
            "RIOT_MCP_MAX_RESULT_SIZE": "4096",
            "RIOT_MCP_MAX_RETAINED_BYTES": "16384",
        }
    )

    assert settings.api_key == "RGAPI-private"
    assert settings.inline_limit == 1024
    assert settings.max_results == 12
    assert settings.result_ttl == 45.5
    assert settings.max_result_size == 4096
    assert settings.max_retained_bytes == 16384


def test_settings_use_safe_backward_compatible_result_defaults() -> None:
    settings = RiotMcpSettings.from_env({"RIOT_API_KEY": "RGAPI-private"})

    assert settings.max_result_size == DEFAULT_MAX_RESULT_SIZE
    assert settings.max_retained_bytes == DEFAULT_MAX_RETAINED_BYTES
    assert settings.max_retained_bytes >= settings.max_result_size


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        ("RIOT_MCP_INLINE_LIMIT", "invalid", "integer"),
        ("RIOT_MCP_MAX_RESULTS", "0", "capacity"),
        ("RIOT_MCP_RESULT_TTL", "nan", "TTL"),
        ("RIOT_MCP_MAX_RESULT_SIZE", "1", "size ceiling"),
        ("RIOT_MCP_MAX_RETAINED_BYTES", "1", "retained-byte"),
    ],
)
def test_settings_reject_invalid_result_limits(
    name: str,
    value: str,
    message: str,
) -> None:
    with pytest.raises(McpConfigurationError, match=message):
        RiotMcpSettings.from_env(
            {
                "RIOT_API_KEY": "RGAPI-private",
                name: value,
            }
        )
