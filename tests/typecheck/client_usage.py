from riotskillissue import (
    MatchSummary,
    PlatformRoute,
    PlayerProfile,
    RegionalRoute,
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
