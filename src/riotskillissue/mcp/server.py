"""MCP SDK integration and stdio server factory."""

from __future__ import annotations

import inspect
import logging
import re
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, TypeVar

from mcp.server import MCPServer
from mcp.server.mcpserver import Context, Elicit, Resolve
from mcp.shared.exceptions import MCPError
from mcp_types import INTERNAL_ERROR, INVALID_PARAMS, ToolAnnotations

from riotskillissue import __version__

from .errors import (
    IntegrationContractError,
    McpConfigurationError,
    McpSecurityError,
    sanitize_exception,
)
from .models import (
    ChallengesRequest,
    ChampionMasteryRequest,
    FindOperationsResult,
    GameContentRequest,
    LeaderboardRequest,
    LiveGameRequest,
    LolItemEconomyRequest,
    LolKnowledgeRequest,
    LolMatchContextRequest,
    LolPlayerContextRequest,
    MatchHistoryRequest,
    OperationDescription,
    PlayerProfileRequest,
    RankedEntriesRequest,
    ResultPage,
    ServiceStatusRequest,
    ToolResult,
    WriteConfirmation,
)
from .operations import OperationGateway, load_operation_registry
from .result_store import ResultStore
from .settings import RiotMcpSettings
from .workflows import WorkflowDispatcher

logger = logging.getLogger(__name__)
_ResultT = TypeVar("_ResultT")
ClientFactory = Callable[[RiotMcpSettings], Any | Awaitable[Any]]


@dataclass(frozen=True)
class McpAppContext:
    """Shared objects held for one MCP server lifespan."""

    client: Any
    result_store: ResultStore
    operations: OperationGateway
    workflows: WorkflowDispatcher
    settings: RiotMcpSettings


def create_server(
    *,
    settings: RiotMcpSettings | None = None,
    client_factory: ClientFactory | None = None,
    registry: object | None = None,
) -> MCPServer[McpAppContext]:
    """Create a local-only RiotSkillIssue MCP server."""
    resolved_settings = settings or RiotMcpSettings.from_env()
    make_client = client_factory or _default_client_factory

    @asynccontextmanager
    async def lifespan(
        server: MCPServer[McpAppContext],
    ) -> AsyncIterator[McpAppContext]:
        del server
        client, exit_client = await _open_client(make_client, resolved_settings)
        try:
            result_store = ResultStore(
                inline_limit=resolved_settings.inline_limit,
                max_results=resolved_settings.max_results,
                ttl=resolved_settings.result_ttl,
                max_result_size=resolved_settings.max_result_size,
                max_retained_bytes=resolved_settings.max_retained_bytes,
            )
            operation_source = registry if registry is not None else load_operation_registry()
            operations = OperationGateway(
                client,
                result_store,
                operation_source,
                allow_writes=resolved_settings.allow_writes,
            )
            yield McpAppContext(
                client=client,
                result_store=result_store,
                operations=operations,
                workflows=WorkflowDispatcher(client, result_store),
                settings=resolved_settings,
            )
        finally:
            await exit_client()

    server = MCPServer[McpAppContext](
        "RiotSkillIssue",
        version=__version__,
        instructions=(
            "For League match questions, use riot_lol_match_context with either a match "
            "ID or Riot ID. Use riot_lol_player_context for combined profile, ranked, "
            "mastery, and recent-match evidence, and riot_lol_knowledge for mechanics "
            "and patch-banded economy guidance. For item gold efficiency, use "
            "riot_lol_item_economy with an exact item name or ID and the match or patch. "
            "Combine economy, minion, experience, structure, and wave-management knowledge "
            "with match checkpoints for strategic questions. Use riot_game_content with the "
            "same patch for abilities, items, runes, and spells. Treat inferred impact "
            "separately from observed Riot data. Use the other high-level tools for common "
            "lookups and operation discovery for complete read-only API coverage. Large "
            "results return an in-memory handle for paginated reads."
        ),
        lifespan=lifespan,
        log_level="WARNING",
    )
    _register_read_tools(server)
    if resolved_settings.allow_writes:
        _register_write_tool(server)
    return server


def _register_read_tools(server: MCPServer[McpAppContext]) -> None:
    read_annotations = ToolAnnotations(read_only_hint=True, open_world_hint=True)

    @server.tool(
        name="riot_lol_match_context",
        title="Analyze League match context",
        annotations=read_annotations,
    )
    async def riot_lol_match_context(
        request: LolMatchContextRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get evidence-rich League match and timeline context for a question."""
        return await _run_tool(lambda: _app(ctx).workflows.call("lol_match_context", request))

    @server.tool(
        name="riot_lol_player_context",
        title="Analyze League player context",
        annotations=read_annotations,
    )
    async def riot_lol_player_context(
        request: LolPlayerContextRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get bounded League profile, ranked, mastery, and recent-match context."""
        return await _run_tool(lambda: _app(ctx).workflows.call("lol_player_context", request))

    @server.tool(
        name="riot_lol_knowledge",
        title="Get League mechanics knowledge",
        annotations=read_annotations,
    )
    async def riot_lol_knowledge(
        request: LolKnowledgeRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get League fundamentals, metric definitions, and analysis limitations."""
        return await _run_tool(lambda: _app(ctx).workflows.call("lol_knowledge", request))

    @server.tool(
        name="riot_lol_item_economy",
        title="Calculate League item raw-stat efficiency",
        annotations=read_annotations,
    )
    async def riot_lol_item_economy(
        request: LolItemEconomyRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Calculate patch-matched component-baseline raw-stat efficiency."""
        return await _run_tool(lambda: _app(ctx).workflows.call("lol_item_economy", request))

    @server.tool(
        name="riot_player_profile",
        title="Get Riot player profile",
        annotations=read_annotations,
    )
    async def riot_player_profile(
        request: PlayerProfileRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get account identity and the available game-specific profile."""
        return await _run_tool(lambda: _app(ctx).workflows.call("player_profile", request))

    @server.tool(
        name="riot_match_history",
        title="Get Riot match history",
        annotations=read_annotations,
    )
    async def riot_match_history(
        request: MatchHistoryRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get a bounded player-centric match history."""
        return await _run_tool(lambda: _app(ctx).workflows.call("match_history", request))

    @server.tool(
        name="riot_ranked_entries",
        title="Get Riot ranked entries",
        annotations=read_annotations,
    )
    async def riot_ranked_entries(
        request: RankedEntriesRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get ranked entries for a League or TFT player."""
        return await _run_tool(lambda: _app(ctx).workflows.call("ranked_entries", request))

    @server.tool(
        name="riot_leaderboard",
        title="Get Riot leaderboard",
        annotations=read_annotations,
    )
    async def riot_leaderboard(
        request: LeaderboardRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get a VALORANT or Legends of Runeterra leaderboard."""
        return await _run_tool(lambda: _app(ctx).workflows.call("leaderboard", request))

    @server.tool(
        name="riot_live_game",
        title="Get Riot live game",
        annotations=read_annotations,
    )
    async def riot_live_game(
        request: LiveGameRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get the current League or TFT game for a player."""
        return await _run_tool(lambda: _app(ctx).workflows.call("live_game", request))

    @server.tool(
        name="riot_champion_mastery",
        title="Get League champion mastery",
        annotations=read_annotations,
    )
    async def riot_champion_mastery(
        request: ChampionMasteryRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get League champion mastery for a player."""
        return await _run_tool(lambda: _app(ctx).workflows.call("champion_mastery", request))

    @server.tool(
        name="riot_challenges",
        title="Get League challenges",
        annotations=read_annotations,
    )
    async def riot_challenges(
        request: ChallengesRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get League challenge progress for a player."""
        return await _run_tool(lambda: _app(ctx).workflows.call("challenges", request))

    @server.tool(
        name="riot_service_status",
        title="Get Riot service status",
        annotations=read_annotations,
    )
    async def riot_service_status(
        request: ServiceStatusRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get status incidents and maintenance for a game."""
        return await _run_tool(lambda: _app(ctx).workflows.call("service_status", request))

    @server.tool(
        name="riot_game_content",
        title="Get Riot game content",
        annotations=read_annotations,
    )
    async def riot_game_content(
        request: GameContentRequest,
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Get League static, VALORANT, or Riftbound content."""
        return await _run_tool(lambda: _app(ctx).workflows.call("game_content", request))

    @server.tool(
        name="riot_find_operations",
        title="Find Riot API operations",
        annotations=read_annotations,
    )
    async def riot_find_operations(
        ctx: Context[McpAppContext, Any],
        query: str = "",
        game: str | None = None,
        include_writes: bool = False,
        limit: int = 20,
    ) -> FindOperationsResult:
        """Search all MCP-eligible generated and Data Dragon operations."""
        return await _run_tool(
            lambda: _app(ctx).operations.find(
                query=query,
                game=game,
                include_writes=include_writes,
                limit=limit,
            )
        )

    @server.tool(
        name="riot_describe_operation",
        title="Describe Riot API operation",
        annotations=read_annotations,
    )
    async def riot_describe_operation(
        operation: str,
        ctx: Context[McpAppContext, Any],
    ) -> OperationDescription:
        """Get routing and argument details for one exposed operation."""
        return await _run_tool(lambda: _app(ctx).operations.describe(operation))

    @server.tool(
        name="riot_call_read_operation",
        title="Call Riot API read operation",
        annotations=read_annotations,
    )
    async def riot_call_read_operation(
        operation: str,
        arguments: dict[str, Any],
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Call an MCP-eligible read operation discovered from the registry."""
        return await _run_tool(lambda: _app(ctx).operations.call_read(operation, arguments))

    @server.tool(
        name="riot_read_result",
        title="Read retained Riot result",
        annotations=read_annotations,
    )
    async def riot_read_result(
        handle: str,
        ctx: Context[McpAppContext, Any],
        pointer: str = "",
        offset: int = 0,
        limit: int = 50,
    ) -> ResultPage:
        """Navigate a retained result with JSON Pointer and pagination."""
        return await _run_tool(
            lambda: _app(ctx).result_store.read(
                handle,
                pointer=pointer,
                offset=offset,
                limit=limit,
            )
        )


def _register_write_tool(server: MCPServer[McpAppContext]) -> None:
    write_annotations = ToolAnnotations(
        read_only_hint=False,
        destructive_hint=True,
        idempotent_hint=False,
        open_world_hint=True,
    )

    @server.tool(
        name="riot_call_write_operation",
        title="Call confirmed Riot API write operation",
        annotations=write_annotations,
    )
    async def riot_call_write_operation(
        operation: str,
        arguments: dict[str, Any],
        confirmation: Annotated[
            WriteConfirmation,
            Resolve(_resolve_write_confirmation),
        ],
        ctx: Context[McpAppContext, Any],
    ) -> ToolResult:
        """Call an eligible write only after resolver-driven human approval."""
        return await _run_tool(
            lambda: _app(ctx).operations.call_write(
                operation,
                arguments,
                confirmed=confirmation.approved,
            )
        )


async def _resolve_write_confirmation(
    operation: str,
) -> WriteConfirmation | Elicit[WriteConfirmation]:
    safe_operation = re.sub(r"[^A-Za-z0-9_.:/-]", "", operation)[:120]
    target = safe_operation or "the requested operation"
    return Elicit(
        f"Allow RiotSkillIssue to call write operation {target!r}?",
        WriteConfirmation,
    )


def _app(ctx: Context[McpAppContext, Any]) -> McpAppContext:
    return ctx.request_context.lifespan_context


async def _run_tool(action: Callable[[], _ResultT | Awaitable[_ResultT]]) -> _ResultT:
    try:
        result = action()
        return await result if inspect.isawaitable(result) else result
    except McpSecurityError as exc:
        raise MCPError(code=INVALID_PARAMS, message=str(exc)) from None
    except (McpConfigurationError, IntegrationContractError) as exc:
        raise MCPError(code=INTERNAL_ERROR, message=str(exc)) from None
    except MCPError:
        raise
    except Exception as exc:
        safe_error = sanitize_exception(exc)
        logger.warning("MCP tool failed with %s", type(exc).__name__)
        raise safe_error from None


async def _open_client(
    factory: ClientFactory,
    settings: RiotMcpSettings,
) -> tuple[Any, Callable[[], Awaitable[None]]]:
    created = factory(settings)
    client = await created if inspect.isawaitable(created) else created
    enter = getattr(client, "__aenter__", None)
    exit_method = getattr(client, "__aexit__", None)
    if callable(enter) and callable(exit_method):
        entered = enter()
        active_client = await entered if inspect.isawaitable(entered) else entered

        async def exit_client() -> None:
            result = exit_method(None, None, None)
            if inspect.isawaitable(result):
                await result

        return active_client, exit_client

    async def close_client() -> None:
        close = getattr(client, "close", None)
        if callable(close):
            result = close()
            if inspect.isawaitable(result):
                await result

    return client, close_client


def _default_client_factory(settings: RiotMcpSettings) -> Any:
    from riotskillissue.core.client import RiotClient

    kwargs: dict[str, Any] = {"api_key": settings.api_key}
    if settings.default_route is not None:
        kwargs["default_route"] = settings.default_route
    return RiotClient(**kwargs)
