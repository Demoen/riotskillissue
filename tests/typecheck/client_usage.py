from pathlib import Path

from riotskillissue import (
    ClientReplay,
    LeagueReplayClient,
    MatchSummary,
    PlatformRoute,
    PlayerProfile,
    RegionalRoute,
    ReplayFile,
    RiotClient,
    SyncRiotClient,
)
from riotskillissue.models.lol.match_v5 import Match


async def async_usage(client: RiotClient) -> tuple[PlayerProfile, list[MatchSummary], Match]:
    profile = await client.lol.player_profile(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )
    history = await client.lol.match_history(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )
    match = await client.raw.lol.match.get_match(
        match_id="EUW1_1",
        route=RegionalRoute.EUROPE,
    )
    return profile, history, match


def sync_usage(client: SyncRiotClient) -> tuple[PlayerProfile, list[MatchSummary], Match]:
    profile = client.lol.player_profile(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )
    history = client.lol.match_history(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )
    match = client.raw.lol.match.get_match(
        match_id="EUW1_1",
        route=RegionalRoute.EUROPE,
    )
    return profile, history, match


async def async_replay_usage(client: RiotClient) -> tuple[list[ReplayFile], Path]:
    files = await client.lol.replays(route=RegionalRoute.EUROPE)
    destination = await client.lol.download_replay(files[0], Path("replays") / files[0].filename)
    return files, destination


def sync_replay_usage(client: SyncRiotClient) -> tuple[list[ReplayFile], Path]:
    files = client.lol.replays(route=RegionalRoute.EUROPE)
    destination = client.lol.download_replay(files[0], Path("replays") / files[0].filename)
    return files, destination


async def local_replay_usage(client: LeagueReplayClient) -> tuple[list[ClientReplay], Path]:
    files = await client.player_replays("Player#EUW")
    destination = await client.download_replay(files[0])
    return files, destination
