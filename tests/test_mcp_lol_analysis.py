from __future__ import annotations

import json
from copy import deepcopy
from types import SimpleNamespace
from typing import Any

import pytest

from riotskillissue.mcp.errors import IntegrationContractError
from riotskillissue.mcp.models import (
    LolItemEconomyRequest,
    LolKnowledgeRequest,
    LolMatchContextRequest,
    LolPlayerContextRequest,
)
from riotskillissue.mcp.lol import LolAnalysisService


POSITIONS = ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY")
CHAMPIONS = (
    "Garen",
    "Nunu",
    "Ahri",
    "Jinx",
    "Thresh",
    "Darius",
    "LeeSin",
    "Syndra",
    "Caitlyn",
    "Leona",
)


def _participant(
    participant_id: int,
    *,
    kills: int,
    deaths: int,
    assists: int,
    win: bool,
    game_name: str | None = None,
) -> dict[str, Any]:
    team_id = 100 if participant_id <= 5 else 200
    index = participant_id - 1
    position = POSITIONS[index % 5]
    champion = CHAMPIONS[index]
    farming = 34 if position == "JUNGLE" else 168 + index * 4
    neutral = 142 + index if position == "JUNGLE" else 8 + index
    return {
        "participantId": participant_id,
        "puuid": "target-puuid" if participant_id == 2 else f"puuid-{participant_id}",
        "riotIdGameName": game_name or f"Player{participant_id}",
        "riotIdTagline": "EUW",
        "summonerName": game_name or f"Player{participant_id}",
        "teamId": team_id,
        "championId": 20 + index,
        "championName": champion,
        "champLevel": 16 if win else 14,
        "teamPosition": position,
        "individualPosition": position,
        "lane": "JUNGLE" if position == "JUNGLE" else position,
        "role": "SUPPORT" if position == "UTILITY" else "SOLO",
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "doubleKills": 1 if kills >= 5 else 0,
        "tripleKills": 0,
        "quadraKills": 0,
        "pentaKills": 0,
        "largestKillingSpree": min(kills, 4),
        "firstBloodKill": participant_id == 3,
        "firstBloodAssist": participant_id == 2,
        "win": win,
        "goldEarned": 12_500 + kills * 350 + assists * 90,
        "goldSpent": 11_800 + kills * 310,
        "totalMinionsKilled": farming,
        "neutralMinionsKilled": neutral,
        "totalDamageDealtToChampions": 14_000 + kills * 1_450,
        "physicalDamageDealtToChampions": 8_000 + kills * 900,
        "magicDamageDealtToChampions": 5_000 + kills * 500,
        "trueDamageDealtToChampions": 1_000 + kills * 50,
        "totalDamageTaken": 17_000 + deaths * 1_100,
        "damageSelfMitigated": 9_000 + deaths * 600,
        "damageDealtToObjectives": 8_500 if position == "JUNGLE" else 2_000,
        "damageDealtToTurrets": 2_600 if win else 700,
        "visionScore": 36 if position == "UTILITY" else 21,
        "wardsPlaced": 22 if position == "UTILITY" else 10,
        "wardsKilled": 6 if position == "UTILITY" else 3,
        "detectorWardsPlaced": 4 if position in {"JUNGLE", "UTILITY"} else 1,
        "timeCCingOthers": 28 if position in {"JUNGLE", "UTILITY"} else 9,
        "objectivesStolen": 0,
        "objectivesStolenAssists": 0,
        "item0": 6630 if participant_id == 2 else 3078,
        "item1": 3047,
        "item2": 3065,
        "item3": 0,
        "item4": 0,
        "item5": 0,
        "item6": 3340,
        "summoner1Id": 11 if position == "JUNGLE" else 4,
        "summoner2Id": 4 if position == "JUNGLE" else 12,
        "challenges": {
            "killParticipation": round((kills + assists) / (22 if win else 15), 3),
            "goldPerMinute": 425.5,
            "damagePerMinute": 650.0,
            "jungleCsBefore10Minutes": 62.0 if position == "JUNGLE" else 0.0,
        },
    }


def make_match(
    match_id: str = "EUW1_9001",
    *,
    target_win: bool = True,
    game_version: str = "14.10.321.1234",
) -> dict[str, Any]:
    blue_kda = ((3, 3, 8), (7, 2, 9), (5, 4, 10), (6, 3, 7), (1, 3, 15))
    red_kda = ((2, 5, 5), (3, 5, 7), (4, 4, 5), (4, 4, 4), (2, 4, 8))
    if target_win:
        blue_won = True
        blue_stats, red_stats = blue_kda, red_kda
    else:
        blue_won = False
        blue_stats, red_stats = red_kda, blue_kda
    participants = [
        _participant(
            participant_id,
            kills=stats[0],
            deaths=stats[1],
            assists=stats[2],
            win=blue_won if participant_id <= 5 else not blue_won,
            game_name="Analyst" if participant_id == 2 else None,
        )
        for participant_id, stats in enumerate((*blue_stats, *red_stats), 1)
    ]
    blue_objectives = {
        "baron": {"first": False, "kills": 0},
        "champion": {"first": True, "kills": sum(item[0] for item in blue_stats)},
        "dragon": {"first": False, "kills": 2},
        "horde": {"first": True, "kills": 3},
        "inhibitor": {"first": True, "kills": 1},
        "riftHerald": {"first": False, "kills": 0},
        "tower": {"first": True, "kills": 7},
    }
    red_objectives = {
        "baron": {"first": True, "kills": 1},
        "champion": {"first": False, "kills": sum(item[0] for item in red_stats)},
        "dragon": {"first": True, "kills": 2},
        "horde": {"first": False, "kills": 0},
        "inhibitor": {"first": False, "kills": 0},
        "riftHerald": {"first": True, "kills": 1},
        "tower": {"first": False, "kills": 3},
    }
    return {
        "metadata": {
            "dataVersion": "2",
            "matchId": match_id,
            "participants": [participant["puuid"] for participant in participants],
        },
        "info": {
            "gameCreation": 1_715_600_000_000,
            "gameDuration": 1_860,
            "gameEndTimestamp": 1_715_601_860_000,
            "gameId": int(match_id.rsplit("_", 1)[-1]),
            "gameMode": "CLASSIC",
            "gameName": "teambuilder-match-9001",
            "gameStartTimestamp": 1_715_600_000_000,
            "gameType": "MATCHED_GAME",
            "gameVersion": game_version,
            "mapId": 11,
            "platformId": match_id.split("_", 1)[0],
            "queueId": 420,
            "tournamentCode": "",
            "participants": participants,
            "teams": [
                {
                    "teamId": 100,
                    "win": blue_won,
                    "bans": [{"championId": 55, "pickTurn": 1}],
                    "objectives": blue_objectives,
                },
                {
                    "teamId": 200,
                    "win": not blue_won,
                    "bans": [{"championId": 64, "pickTurn": 2}],
                    "objectives": red_objectives,
                },
            ],
        },
    }


def _participant_frame(
    participant_id: int,
    timestamp: int,
    total_gold: int,
) -> dict[str, Any]:
    position = {"x": 5_000 + participant_id * 350, "y": 5_200 + participant_id * 280}
    return {
        "participantId": participant_id,
        "position": position,
        "currentGold": max(0, total_gold - 4_000),
        "totalGold": total_gold,
        "level": min(18, 1 + timestamp // 120_000),
        "xp": timestamp // 12,
        "minionsKilled": timestamp // 7_500,
        "jungleMinionsKilled": timestamp // 5_500 if participant_id in {2, 7} else 4,
        "timeEnemySpentControlled": participant_id * 250,
        "goldPerSecond": 0,
        "championStats": {
            "abilityHaste": 10,
            "abilityPower": 0,
            "armor": 50,
            "attackDamage": 100,
            "attackSpeed": 110,
            "health": 1_500,
            "healthMax": 1_700,
            "healthRegen": 12,
            "magicResist": 38,
            "movementSpeed": 350,
            "power": 600,
            "powerMax": 800,
            "powerRegen": 15,
        },
        "damageStats": {
            "magicDamageDone": 2_000,
            "magicDamageDoneToChampions": 800,
            "magicDamageTaken": 600,
            "physicalDamageDone": 5_000,
            "physicalDamageDoneToChampions": 1_200,
            "physicalDamageTaken": 1_100,
            "totalDamageDone": 7_200,
            "totalDamageDoneToChampions": 2_100,
            "totalDamageTaken": 1_800,
            "trueDamageDone": 200,
            "trueDamageDoneToChampions": 100,
            "trueDamageTaken": 100,
        },
    }


def _frame(
    timestamp: int,
    blue_total: int,
    red_total: int,
    events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    blue = [blue_total // 5 + offset for offset in (-160, -80, 0, 80, 160)]
    red = [red_total // 5 + offset for offset in (-160, -80, 0, 80, 160)]
    frames = {
        str(participant_id): _participant_frame(participant_id, timestamp, gold)
        for participant_id, gold in enumerate((*blue, *red), 1)
    }
    return {"timestamp": timestamp, "participantFrames": frames, "events": events or []}


def make_timeline(match_id: str = "EUW1_9001") -> dict[str, Any]:
    horde_events = [
        {
            "type": "ELITE_MONSTER_KILL",
            "timestamp": timestamp,
            "killerId": 2,
            "killerTeamId": 100,
            "assistingParticipantIds": [1, 3, 5],
            "monsterType": "HORDE",
            "monsterSubType": "VOID_GRUB",
            "position": {"x": 4_350, "y": 9_600},
        }
        for timestamp in (390_000, 410_000, 430_000)
    ]
    conversion_events = [
        {
            "type": "CHAMPION_KILL",
            "timestamp": 445_000,
            "killerId": 2,
            "victimId": 7,
            "assistingParticipantIds": [3, 5],
            "bounty": 300,
            "killStreakLength": 1,
            "position": {"x": 5_100, "y": 9_250},
        },
        {
            "type": "ELITE_MONSTER_KILL",
            "timestamp": 470_000,
            "killerId": 7,
            "killerTeamId": 200,
            "assistingParticipantIds": [8, 9, 10],
            "monsterType": "DRAGON",
            "monsterSubType": "AIR_DRAGON",
            "position": {"x": 9_800, "y": 4_400},
        },
        {
            "type": "BUILDING_KILL",
            "timestamp": 505_000,
            "killerId": 3,
            "assistingParticipantIds": [1, 2, 5],
            "teamId": 200,
            "buildingType": "TOWER_BUILDING",
            "towerType": "OUTER_TURRET",
            "laneType": "MID_LANE",
            "position": {"x": 8_950, "y": 8_500},
        },
        {
            "type": "ITEM_PURCHASED",
            "timestamp": 520_000,
            "participantId": 2,
            "itemId": 6630,
        },
    ]
    later_events = [
        {
            "type": "CHAMPION_KILL",
            "timestamp": 720_000,
            "killerId": 9,
            "victimId": 4,
            "assistingParticipantIds": [7, 10],
            "position": {"x": 10_200, "y": 7_900},
        },
        {
            "type": "BUILDING_KILL",
            "timestamp": 780_000,
            "killerId": 1,
            "assistingParticipantIds": [2, 3],
            "teamId": 200,
            "buildingType": "TOWER_BUILDING",
            "towerType": "INNER_TURRET",
            "laneType": "TOP_LANE",
            "position": {"x": 8_100, "y": 10_500},
        },
    ]
    return {
        "metadata": {
            "dataVersion": "2",
            "matchId": match_id,
            "participants": [
                "target-puuid" if participant_id == 2 else f"puuid-{participant_id}"
                for participant_id in range(1, 11)
            ],
        },
        "info": {
            "frameInterval": 60_000,
            "frames": [
                _frame(0, 2_500, 2_500),
                _frame(360_000, 10_500, 11_000),
                _frame(480_000, 15_000, 14_500, horde_events + conversion_events),
                _frame(600_000, 20_000, 18_000),
                _frame(720_000, 25_000, 22_500, later_events),
                _frame(900_000, 32_000, 28_500),
                _frame(1_200_000, 44_000, 39_000),
                _frame(1_500_000, 57_000, 50_000),
                _frame(1_860_000, 71_000, 62_000),
            ],
        },
    }


class StaticDouble:
    def __init__(self, *, failure: BaseException | None = None) -> None:
        self.failure = failure
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def _result(self, name: str, values: Any, **kwargs: Any) -> Any:
        self.calls.append((name, kwargs))
        if self.failure is not None:
            raise self.failure
        return deepcopy(values)

    async def get_versions(self) -> list[str]:
        return await self._result(
            "get_versions",
            ["16.15.1", "14.10.1", "14.9.1", "14.1.1"],
        )

    async def get_latest_version(self) -> str:
        return await self._result("get_latest_version", "16.15.1")

    async def resolve_version(self, game_version: str | None = None) -> str:
        return await self._result(
            "resolve_version",
            "14.10.1" if str(game_version).startswith("14.10") else "16.15.1",
            game_version=game_version,
        )

    async def get_all_champions(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> dict[int, dict[str, Any]]:
        return await self._result(
            "get_all_champions",
            {
                20 + index: {
                    "id": champion,
                    "key": str(20 + index),
                    "name": champion,
                    "title": f"the synthetic {champion}",
                    "tags": ["Fighter"],
                }
                for index, champion in enumerate(CHAMPIONS)
            },
            version=version,
            locale=locale,
        )

    async def get_all_items(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> dict[int, dict[str, Any]]:
        return await self._result(
            "get_all_items",
            {
                3047: {"name": "Plated Steelcaps", "gold": {"total": 1_200}},
                3065: {"name": "Spirit Visage", "gold": {"total": 2_700}},
                3078: {"name": "Trinity Force", "gold": {"total": 3_333}},
                3340: {"name": "Stealth Ward", "gold": {"total": 0}},
                6630: {"name": "Stridebreaker", "gold": {"total": 3_300}},
            },
            version=version,
            locale=locale,
        )

    async def get_item_efficiency(
        self,
        item_id: int | None = None,
        *,
        item_name: str | None = None,
        game_version: str | None = None,
        locale: str = "en_US",
        map_id: int | None = 11,
    ) -> dict[str, Any]:
        return await self._result(
            "get_item_efficiency",
            {
                "patch": {"resolved_data_dragon_version": "16.15.1"},
                "item": {"id": item_id, "name": item_name},
                "raw_stat_efficiency_percent": 100.0,
            },
            item_id=item_id,
            item_name=item_name,
            game_version=game_version,
            locale=locale,
            map_id=map_id,
        )

    async def get_summoner_spells(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> dict[int, dict[str, Any]]:
        return await self._result(
            "get_summoner_spells",
            {
                4: {"name": "Flash", "key": "4"},
                11: {"name": "Smite", "key": "11"},
                12: {"name": "Teleport", "key": "12"},
            },
            version=version,
            locale=locale,
        )

    async def get_runes(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> list[dict[str, Any]]:
        return await self._result(
            "get_runes",
            [
                {
                    "id": 8000,
                    "key": "Precision",
                    "name": "Precision",
                    "slots": [{"runes": [{"id": 8010, "key": "Conqueror", "name": "Conqueror"}]}],
                }
            ],
            version=version,
            locale=locale,
        )

    async def get_queues(self) -> list[dict[str, Any]]:
        return await self._result(
            "get_queues",
            [{"queueId": 420, "map": "Summoner's Rift", "description": "Ranked Solo"}],
        )

    async def get_maps(self) -> list[dict[str, Any]]:
        return await self._result("get_maps", [{"mapId": 11, "mapName": "Summoner's Rift"}])


class ClientDouble:
    def __init__(
        self,
        *,
        matches: dict[str, dict[str, Any]] | None = None,
        timelines: dict[str, dict[str, Any] | BaseException] | None = None,
        match_ids: list[str] | None = None,
        match_failures: set[str] | None = None,
        static_failure: BaseException | None = None,
    ) -> None:
        base_match = make_match()
        self.matches = matches or {"EUW1_9001": base_match}
        self.timelines = timelines or {"EUW1_9001": make_timeline()}
        self.match_ids = match_ids or list(self.matches)
        self.match_failures = match_failures or set()
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.static = StaticDouble(failure=static_failure)
        self.lol = SimpleNamespace(
            player_profile=self.player_profile,
            match_ids=self.high_level_match_ids,
            ranked_entries=self.ranked_entries,
            champion_mastery=self.champion_mastery,
        )
        match_api = SimpleNamespace(
            get_match=self.get_match,
            get_timeline=self.get_timeline,
            get_match_ids_by_puuid=self.get_match_ids_by_puuid,
        )
        account_api = SimpleNamespace(get_by_riot_id=self.get_by_riot_id)
        self.raw = SimpleNamespace(
            lol=SimpleNamespace(match=match_api),
            common=SimpleNamespace(account=account_api),
            call_operation=self.call_operation,
        )

    async def call_operation(
        self,
        operation: str,
        arguments: dict[str, Any],
    ) -> Any:
        self.calls.append((operation, dict(arguments)))
        normalized = operation.casefold()
        if "getbyriotid" in normalized:
            return await self.get_by_riot_id(**arguments, _record=False)
        if "getmatchidsbypuuid" in normalized:
            return await self.get_match_ids_by_puuid(**arguments, _record=False)
        if normalized.endswith("gettimeline"):
            return await self.get_timeline(**arguments, _record=False)
        if normalized.endswith("getmatch"):
            return await self.get_match(**arguments, _record=False)
        if "leagueentries" in normalized:
            return await self.ranked_entries("Analyst#EUW", _record=False, **arguments)
        if "championmaster" in normalized:
            return await self.champion_mastery("Analyst#EUW", _record=False, **arguments)
        if "challenges" in normalized and "playerdata" in normalized:
            return {"totalPoints": {"level": "GOLD", "current": 8_200, "max": 12_000}}
        if "summoner" in normalized and "getbypuuid" in normalized:
            return {"puuid": "target-puuid", "summonerLevel": 412, "profileIconId": 29}
        raise AssertionError(f"Unexpected operation: {operation} {arguments}")

    async def get_by_riot_id(
        self,
        *,
        game_name: str,
        tag_line: str,
        route: str | None = None,
        _record: bool = True,
    ) -> dict[str, str]:
        if _record:
            self.calls.append(
                (
                    "account-v1.getByRiotId",
                    {"game_name": game_name, "tag_line": tag_line, "route": route},
                )
            )
        return {"puuid": "target-puuid", "gameName": game_name, "tagLine": tag_line}

    async def get_match_ids_by_puuid(
        self,
        *,
        puuid: str,
        route: str | None = None,
        count: int | None = None,
        start: int | None = None,
        _record: bool = True,
        **kwargs: Any,
    ) -> list[str]:
        arguments = {
            "puuid": puuid,
            "route": route,
            "count": count,
            "start": start,
            **kwargs,
        }
        if _record:
            self.calls.append(("match-v5.getMatchIdsByPUUID", arguments))
        offset = start or 0
        limit = count if count is not None else len(self.match_ids)
        return self.match_ids[offset : offset + limit]

    async def get_match(
        self,
        *,
        match_id: str,
        route: str | None = None,
        _record: bool = True,
    ) -> dict[str, Any]:
        if _record:
            self.calls.append(("match-v5.getMatch", {"match_id": match_id, "route": route}))
        if match_id in self.match_failures:
            raise RuntimeError(f"match unavailable: {match_id}")
        return deepcopy(self.matches[match_id])

    async def get_timeline(
        self,
        *,
        match_id: str,
        route: str | None = None,
        _record: bool = True,
    ) -> dict[str, Any]:
        if _record:
            self.calls.append(("match-v5.getTimeline", {"match_id": match_id, "route": route}))
        value = self.timelines[match_id]
        if isinstance(value, BaseException):
            raise value
        return deepcopy(value)

    async def player_profile(
        self,
        riot_id: str,
        *,
        route: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("lol.player_profile", {"riot_id": riot_id, "route": route}))
        game_name, tag_line = riot_id.split("#", 1)
        return {
            "game": "lol",
            "riot_id": riot_id,
            "puuid": "target-puuid",
            "account": {"puuid": "target-puuid", "gameName": game_name, "tagLine": tag_line},
            "game_profile": {"summonerLevel": 412, "profileIconId": 29},
        }

    async def high_level_match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        start: int = 0,
        route: str | None = None,
        **kwargs: Any,
    ) -> list[str]:
        self.calls.append(
            (
                "lol.match_ids",
                {"riot_id": riot_id, "count": count, "start": start, "route": route, **kwargs},
            )
        )
        return self.match_ids[start : start + count]

    async def ranked_entries(
        self,
        riot_id: str,
        *,
        route: str | None = None,
        _record: bool = True,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        if _record:
            self.calls.append(
                ("lol.ranked_entries", {"riot_id": riot_id, "route": route, **kwargs})
            )
        return [
            {
                "queueType": "RANKED_SOLO_5x5",
                "tier": "EMERALD",
                "rank": "II",
                "leaguePoints": 63,
                "wins": 74,
                "losses": 68,
            }
        ]

    async def champion_mastery(
        self,
        riot_id: str,
        *,
        route: str | None = None,
        count: int | None = None,
        _record: bool = True,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        if _record:
            self.calls.append(
                (
                    "lol.champion_mastery",
                    {"riot_id": riot_id, "route": route, "count": count, **kwargs},
                )
            )
        return [
            {"championId": 21, "championLevel": 7, "championPoints": 188_000},
            {"championId": 22, "championLevel": 6, "championPoints": 91_000},
        ]


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str).casefold()


def _mapping_nodes(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        found.append(value)
        for item in value.values():
            found.extend(_mapping_nodes(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_mapping_nodes(item))
    return found


def _values_for_keys(value: Any, *keys: str) -> list[Any]:
    normalized = {key.casefold().replace("_", "") for key in keys}
    return [
        item
        for node in _mapping_nodes(value)
        for key, item in node.items()
        if key.casefold().replace("_", "") in normalized
    ]


@pytest.mark.asyncio
async def test_swiftplay_26_1_marks_void_grubs_not_applicable() -> None:
    match = make_match(game_version="16.1.1.100")
    match["info"]["queueId"] = 480
    for team in match["info"]["teams"]:
        team["objectives"].pop("horde")
    client = ClientDouble(matches={"EUW1_9001": match})

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id="EUW1_9001", include_timeline=False)
    )

    grubs = result["impact_assessments"]["void_grubs"]
    assert grubs["applicable"] is False
    assert grubs["assessment"]["classification"] == "not_applicable"
    assert "swiftplay" in grubs["applicability_reason"].casefold()


@pytest.mark.asyncio
async def test_missing_grub_objectives_without_timeline_is_unknown_not_zero() -> None:
    match = make_match()
    for team in match["info"]["teams"]:
        team["objectives"].pop("horde")
    client = ClientDouble(matches={"EUW1_9001": match})

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id="EUW1_9001", include_timeline=False)
    )

    grubs = result["impact_assessments"]["void_grubs"]
    assert grubs["telemetry_available"] is False
    assert grubs["observed"]["team_counts"] == {"100": None, "200": None}
    assert grubs["assessment"]["classification"] == "telemetry_unavailable"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("platform", "regional"),
    (("NA1", "americas"), ("KR", "asia"), ("EUW1", "europe"), ("SG2", "sea")),
)
async def test_direct_match_id_infers_regional_route(
    platform: str,
    regional: str,
) -> None:
    match_id = f"{platform}_9001"
    client = ClientDouble(matches={match_id: make_match(match_id)})

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id=match_id, include_timeline=False)
    )

    assert result["match"]["match_id"] == match_id
    assert result["match"]["route"] == regional
    match_calls = [
        arguments for operation, arguments in client.calls if operation == "match-v5.getMatch"
    ]
    assert match_calls == [{"match_id": match_id, "route": regional}]
    assert all(operation != "match-v5.getTimeline" for operation, _ in client.calls)


@pytest.mark.asyncio
@pytest.mark.parametrize("platform", ("sg2", "oc1", "ph2", "th2", "tw2", "vn2"))
async def test_sea_riot_id_match_resolution_splits_account_and_match_routes(
    platform: str,
) -> None:
    match_id = f"{platform.upper()}_9010"
    client = ClientDouble(
        matches={match_id: make_match(match_id)},
        match_ids=[match_id],
    )

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(
            riot_id="Analyst#SEA",
            route=platform,
            include_timeline=False,
        )
    )

    assert result["match"]["route"] == "sea"
    assert (
        "account-v1.getByRiotId",
        {
            "game_name": "Analyst",
            "tag_line": "SEA",
            "route": "asia",
        },
    ) in client.calls
    assert (
        "match-v5.getMatchIdsByPUUID",
        {
            "puuid": "target-puuid",
            "start": 0,
            "count": 1,
            "route": "sea",
        },
    ) in client.calls
    assert (
        "match-v5.getMatch",
        {"match_id": match_id, "route": "sea"},
    ) in client.calls


@pytest.mark.asyncio
async def test_sea_player_context_preserves_platform_and_splits_regional_routes() -> None:
    match_id = "SG2_9011"
    client = ClientDouble(
        matches={match_id: make_match(match_id)},
        match_ids=[match_id],
    )

    result = await LolAnalysisService(client).player_context(
        LolPlayerContextRequest(
            riot_id="Analyst#SEA",
            route="sg2",
            count=1,
        )
    )

    assert result["identity"]["platform_route"] == "sg2"
    assert (
        "account-v1.getByRiotId",
        {
            "game_name": "Analyst",
            "tag_line": "SEA",
            "route": "asia",
        },
    ) in client.calls
    platform_operations = {
        "summoner-v4.getByPUUID",
        "league-v4.getLeagueEntriesByPUUID",
        "champion-mastery-v4.getTopChampionMasteriesByPUUID",
        "lol-challenges-v1.getPlayerData",
    }
    platform_calls = [
        (operation, arguments)
        for operation, arguments in client.calls
        if operation in platform_operations
    ]
    assert {operation for operation, _ in platform_calls} == platform_operations
    assert all(arguments["route"] == "sg2" for _, arguments in platform_calls)
    assert (
        "match-v5.getMatchIdsByPUUID",
        {
            "puuid": "target-puuid",
            "start": 0,
            "count": 1,
            "route": "sea",
        },
    ) in client.calls
    assert (
        "match-v5.getMatch",
        {"match_id": match_id, "route": "sea"},
    ) in client.calls


@pytest.mark.asyncio
async def test_riot_id_resolves_latest_match_and_focus_participant() -> None:
    latest_id = "EUW1_9002"
    older_id = "EUW1_9001"
    latest = make_match(latest_id)
    client = ClientDouble(
        matches={latest_id: latest, older_id: make_match(older_id, target_win=False)},
        timelines={latest_id: make_timeline(latest_id)},
        match_ids=[latest_id, older_id],
    )

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(
            riot_id="Analyst#EUW",
            route="euw1",
            match_index=0,
            question="What happened in my latest game?",
        )
    )

    assert result["match"]["match_id"] == latest_id
    assert result["match"]["route"] == "europe"
    assert result["focus_participant"]["riot_id"] == "Analyst#EUW"
    assert "puuid" not in result["focus_participant"]
    assert all("puuid" not in participant for participant in result["participants"])
    assert (
        "match-v5.getMatchIdsByPUUID",
        {
            "puuid": "target-puuid",
            "start": 0,
            "count": 1,
            "route": "europe",
        },
    ) in client.calls
    assert ("match-v5.getMatch", {"match_id": latest_id, "route": "europe"}) in client.calls


@pytest.mark.asyncio
async def test_void_grub_evidence_conversion_and_telemetry_limits() -> None:
    result = await LolAnalysisService(ClientDouble()).match_context(
        LolMatchContextRequest(
            match_id="EUW1_9001",
            question="How much impact did voidgrubs have this game?",
            detail="full",
        )
    )

    grubs = result["impact_assessments"]["void_grubs"]
    assert grubs["available"] is True
    assert grubs["observed"]["team_counts"] == {"100": 3, "200": 0}
    assert grubs["observed"]["timeline_counts"] == {"100": 3, "200": 0}
    assert [capture["timestamp_ms"] for capture in grubs["observed"]["captures"]] == [
        390_000,
        410_000,
        430_000,
    ]
    credited = grubs["observed"]["credited_participants"]
    assert credited[0]["participant"]["riot_id"] == "Analyst#EUW"
    assert credited[0]["credited_capture_events"] == 3

    conversion = grubs["conversion_proxies"]["100"]
    assert conversion["capture_count"] == 3
    assert conversion["first_capture_ms"] == 390_000
    assert conversion["net_gold_swing_next_two_minutes"] > 0
    assert conversion["gold_window"]["baseline"]["target_timestamp_ms"] == 390_000
    assert conversion["gold_window"]["after_two_minutes"]["target_timestamp_ms"] == 510_000
    assert conversion["buildings_destroyed_next_five_minutes"] == 1
    assert conversion["long_horizon_outcomes"]["buildings_destroyed_after_first_capture"] == 2
    conversion_events = conversion["events_next_three_minutes"]
    assert len(conversion_events) == 3
    assert any(
        event["type"] == "CHAMPION_KILL" and event["acting_team_id"] == 100
        for event in conversion_events
    )
    assert any(
        event["type"] == "ELITE_MONSTER_KILL"
        and event["monster_type"] == "DRAGON"
        and event["acting_team_id"] == 200
        for event in conversion_events
    )
    assert any(
        event["type"] == "BUILDING_KILL" and event["acting_team_id"] == 100
        for event in conversion_events
    )
    assert grubs["assessment"]["classification"] == "strong_positive_conversion_association"
    assert grubs["assessment"]["leader_team_id"] == 100
    assert grubs["assessment"]["causal_confidence"] == "not_estimable"
    assert grubs["assessment"]["long_horizon_context"]["scored"] is False
    assert "association" in grubs["causal_limit"].casefold()
    assert "exact causal damage" in grubs["causal_limit"].casefold()

    event_types = {event["type"] for event in result["timeline"]["major_events"]}
    assert {"ELITE_MONSTER_KILL", "CHAMPION_KILL", "BUILDING_KILL"} <= event_types
    assert len(result["timeline"]["item_milestones"]) == 1
    milestone = result["timeline"]["item_milestones"][0]
    assert milestone["timestamp_ms"] == 520_000
    assert milestone["minute"] == pytest.approx(8.67)
    assert milestone["type"] == "ITEM_PURCHASED"
    assert milestone["participant"]["participant_id"] == 2
    assert milestone["participant"]["riot_id"] == "Analyst#EUW"
    assert milestone["participant"]["champion"] == "Nunu"
    assert milestone["participant"]["team_id"] == 100
    assert milestone["item_id"] == 6630
    assert milestone["item_name"] == "Stridebreaker"
    assert "void_grubs" in result["question_relevance"]["detected_topics"]
    quality_text = _json(result["data_quality"])
    assert "not a replay" in quality_text
    assert "causal" in quality_text


@pytest.mark.asyncio
async def test_player_context_aggregates_loaded_matches_and_reports_partial_failure() -> None:
    match_ids = ["EUW1_9001", "EUW1_9002", "EUW1_9003"]
    client = ClientDouble(
        matches={
            match_ids[0]: make_match(match_ids[0], target_win=True),
            match_ids[1]: make_match(match_ids[1], target_win=False),
            match_ids[2]: make_match(match_ids[2], target_win=True),
        },
        match_ids=match_ids,
        match_failures={match_ids[2]},
    )

    result = await LolAnalysisService(client).player_context(
        LolPlayerContextRequest(
            riot_id="Analyst#EUW",
            route="euw1",
            count=3,
            question="How has this jungler performed recently?",
        )
    )

    assert result["identity"] == {
        "riot_id": "Analyst#EUW",
        "game_name": "Analyst",
        "tag_line": "EUW",
        "platform_route": "euw1",
    }
    assert result["summoner"]["summoner_level"] == 412
    assert result["ranked_entries"][0]["tier"] == "EMERALD"
    assert result["ranked_entries"][0]["win_rate"] == pytest.approx(74 / 142, abs=0.001)
    assert [entry["champion_name"] for entry in result["top_champion_mastery"][:2]] == [
        "Nunu",
        "Ahri",
    ]

    recent = result["recent_matches"]
    assert recent["requested"] == 3
    assert recent["ids_returned"] == 3
    assert recent["loaded"] == 2
    assert recent["analyzed"] == 2
    assert recent["returned"] == 2
    assert [match["match_id"] for match in recent["matches"]] == match_ids[:2]
    assert recent["aggregate"]["games"] == 2
    assert recent["aggregate"]["wins"] == 1
    assert recent["aggregate"]["losses"] == 1
    assert recent["aggregate"]["win_rate"] == 0.5
    assert recent["aggregate"]["champions"] == {"Nunu": 2}
    assert recent["aggregate"]["roles"] == {"JUNGLE": 2}
    assert recent["aggregate"]["averages"]["kills"] == 5.0
    assert recent["aggregate"]["averages"]["deaths"] == 3.5
    assert recent["aggregate"]["averages"]["assists"] == 8.0
    assert "not an mmr" in recent["sample_notice"].casefold()

    warnings = result["data_quality"]["warnings"]
    assert result["data_quality"]["optional_sections_may_be_missing"] is True
    normalized_warnings = "".join(
        character for character in " ".join(warnings).casefold() if character.isalnum()
    )
    assert "euw19003" in normalized_warnings
    assert any("unavailable" in warning.casefold() for warning in warnings)
    assert all(
        source["operation"] != "match-v5.getMatch" or source["status"] == "loaded"
        for source in result["provenance"]["sources"]
    )


@pytest.mark.asyncio
async def test_player_summary_reports_loaded_analyzed_and_returned_counts() -> None:
    match_ids = [f"EUW1_{9100 + index}" for index in range(5)]
    client = ClientDouble(
        matches={match_id: make_match(match_id) for match_id in match_ids},
        match_ids=match_ids,
    )

    result = await LolAnalysisService(client).player_context(
        LolPlayerContextRequest(
            riot_id="Analyst#EUW",
            route="euw1",
            count=5,
            detail="summary",
        )
    )

    recent = result["recent_matches"]
    assert recent["loaded"] == 5
    assert recent["analyzed"] == 5
    assert recent["returned"] == 3
    assert recent["aggregate"]["games"] == 5
    assert len(recent["matches"]) == 3


@pytest.mark.asyncio
async def test_match_context_survives_timeline_and_static_enrichment_failures() -> None:
    client = ClientDouble(
        timelines={"EUW1_9001": TimeoutError("timeline timed out")},
        static_failure=RuntimeError("Data Dragon offline"),
    )

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(
            match_id="EUW1_9001",
            question="Did the early objective decide this match?",
        )
    )

    assert result["match"]["match_id"] == "EUW1_9001"
    assert len(result["teams"]) == 2
    assert len(result["participants"]) == 10
    assert result["timeline"] == {
        "checkpoints": [],
        "major_events": [],
        "likely_teamfights": [],
        "item_milestones": [],
    }
    assert result["data_quality"]["timeline_available"] is False
    assert result["data_quality"]["static_version"] is None
    assert result["data_quality"]["static_patch_match"] is None
    warnings = " ".join(result["data_quality"]["warnings"]).casefold()
    assert "timeline" in warnings
    assert "timeouterror" in warnings
    assert "data dragon" in warnings
    assert "runtimeerror" in warnings

    grubs = result["impact_assessments"]["void_grubs"]
    assert grubs["available"] is True
    assert grubs["observed"]["team_counts"] == {"100": 3, "200": 0}
    assert grubs["observed"]["timeline_counts"] == {"100": 0, "200": 0}
    assert grubs["observed"]["captures"] == []
    assert grubs["conversion_proxies"]["100"]["first_capture_ms"] is None
    assert grubs["conversion_proxies"]["100"]["net_gold_swing_next_two_minutes"] is None
    assert grubs["assessment"]["confidence"] == "low"
    assert "association" in grubs["causal_limit"].casefold()


@pytest.mark.asyncio
async def test_match_context_rejects_cross_patch_static_enrichment() -> None:
    class MismatchedStatic(StaticDouble):
        async def resolve_version(self, game_version: str | None = None) -> str:
            return await self._result(
                "resolve_version",
                "16.15.1",
                game_version=game_version,
            )

    client = ClientDouble()
    client.static = MismatchedStatic()

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id="EUW1_9001")
    )

    assert result["data_quality"]["static_version"] is None
    assert result["data_quality"]["rejected_static_version"] == "16.15.1"
    assert result["data_quality"]["static_patch_match"] is False
    assert {name for name, _ in client.static.calls} == {
        "resolve_version",
        "get_queues",
        "get_maps",
    }
    assert (
        "versioned enrichment was omitted"
        in " ".join(result["data_quality"]["warnings"]).casefold()
    )


@pytest.mark.asyncio
async def test_empty_required_match_payload_is_rejected() -> None:
    client = ClientDouble(matches={"EUW1_9001": {}})

    with pytest.raises(IntegrationContractError):
        await LolAnalysisService(client).match_context(
            LolMatchContextRequest(match_id="EUW1_9001", include_timeline=False)
        )


@pytest.mark.asyncio
async def test_empty_timeline_frames_are_unavailable_and_cannot_prove_no_grubs() -> None:
    match = make_match()
    for team in match["info"]["teams"]:
        team["objectives"]["horde"] = {"first": False, "kills": 0}
    empty_timeline = {
        "metadata": {
            "dataVersion": "2",
            "matchId": "EUW1_9001",
            "participants": match["metadata"]["participants"],
        },
        "info": {"frameInterval": 60_000, "frames": []},
    }
    client = ClientDouble(
        matches={"EUW1_9001": match},
        timelines={"EUW1_9001": empty_timeline},
    )

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id="EUW1_9001")
    )

    assert result["data_quality"]["timeline_available"] is False
    assert any("timeline" in warning.casefold() for warning in result["data_quality"]["warnings"])
    assessment = result["impact_assessments"]["void_grubs"]["assessment"]
    assert assessment["classification"] == "no_observed_void_grubs"
    assert assessment["confidence"] != "high"
    assert result["timeline"] == {
        "checkpoints": [],
        "major_events": [],
        "likely_teamfights": [],
        "item_milestones": [],
    }


@pytest.mark.asyncio
async def test_mismatched_timeline_match_id_is_ignored_with_warning() -> None:
    client = ClientDouble(
        timelines={"EUW1_9001": make_timeline("EUW1_9999")},
    )

    result = await LolAnalysisService(client).match_context(
        LolMatchContextRequest(match_id="EUW1_9001")
    )

    assert result["data_quality"]["timeline_available"] is False
    assert any(
        "timeline" in warning.casefold() and "match" in warning.casefold()
        for warning in result["data_quality"]["warnings"]
    )
    assert result["timeline"] == {
        "checkpoints": [],
        "major_events": [],
        "likely_teamfights": [],
        "item_milestones": [],
    }
    grubs = result["impact_assessments"]["void_grubs"]
    assert grubs["observed"]["team_counts"] == {"100": 3, "200": 0}
    assert grubs["observed"]["timeline_counts"] == {"100": 0, "200": 0}
    assert grubs["observed"]["captures"] == []


@pytest.mark.parametrize(
    ("patch", "band", "mechanic"),
    (
        ("13.24", "before_patch_14_1", "not part"),
        ("14.1", "patch_14_1_through_15_8", "six team stacks"),
        ("15.8", "patch_14_1_through_15_8", "six team stacks"),
        ("25.8", "patch_14_1_through_15_8", "six team stacks"),
        ("15.9", "patch_15_9_and_later_2025", "capped at three"),
        ("25.9", "patch_15_9_and_later_2025", "capped at three"),
        ("16.1", "patch_16_1_and_later_2026", "killer heal"),
        ("26.1", "patch_16_1_and_later_2026", "killer heal"),
        ("17.1", "patch_unknown", "patch-sensitive"),
        ("27.1", "patch_unknown", "patch-sensitive"),
    ),
)
def test_void_grub_knowledge_is_patch_banded(
    patch: str,
    band: str,
    mechanic: str,
) -> None:
    result = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(
            topic="void_grubs",
            patch=patch,
            question="How should teams convert this objective?",
        )
    )

    assert result["patch_requested"] == patch
    assert result["knowledge"]["patch_band"] == band
    assert mechanic in " ".join(result["knowledge"]["mechanics"]).casefold()
    assert "capture cost" in _json(result["knowledge"]["impact_framework"])
    assert "exact per-hit buff damage" in result["knowledge"]["telemetry_limit"].casefold()
    assert result["knowledge"]["sources"]
    assert all(source.startswith("https://") for source in result["knowledge"]["sources"])
    assert "objectives" in result["question_relevance"]["detected_topics"]


def test_void_grub_knowledge_marks_unspecified_patch_as_unknown() -> None:
    result = LolAnalysisService(ClientDouble()).knowledge(LolKnowledgeRequest(topic="void_grubs"))

    assert result["patch_requested"] is None
    assert result["knowledge"]["patch_band"] == "patch_unknown"
    assert "patch-sensitive" in _json(result["knowledge"])


def test_current_void_grub_knowledge_has_allocated_direct_rewards() -> None:
    knowledge = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="void_grubs", patch="26.15")
    )["knowledge"]

    assert knowledge["direct_reward_model"]["each_grub"] == {
        "killer_gold": 30,
        "local_xp": 65,
        "xp_radius_units": 2000,
    }
    assert knowledge["direct_reward_model"]["three_grubs"] == {
        "base_gold_total": 90,
        "raw_local_xp_total_before_sharing": 195,
    }
    assert "not 90 per teammate" in knowledge["direct_reward_model"]["allocation_warning"]


def test_knowledge_question_paths_and_summary_detail_match_payload() -> None:
    result = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(
            topic="core",
            question="How do objectives create tempo?",
            detail="summary",
        )
    )

    assert result["question_relevance"]["evidence_paths"] == ["/knowledge"]
    assert len(result["knowledge"]["principles"]) == 2
    assert len(result["knowledge"]["analysis"]) == 2


@pytest.mark.parametrize("patch", (None, "16.15", "26.15"))
def test_minion_economy_has_patch_scoped_gold_xp_and_wave_math(
    patch: str | None,
) -> None:
    result = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="minions", patch=patch)
    )
    knowledge = result["knowledge"]
    examples = {entry["label"]: entry for entry in knowledge["derived_wave_examples"]}

    assert knowledge["patch_identity"]["model_status"] in {"current_reference", "available"}
    assert knowledge["patch_identity"]["mode_scope"].startswith("Map 11 CLASSIC")
    assert knowledge["minion_units"]["melee"] == {
        "last_hit_gold": 20,
        "base_xp": 62,
        "allocation": {"gold": "killer", "xp": "local proximity"},
    }
    assert knowledge["minion_units"]["caster"]["last_hit_gold"] == 14
    assert knowledge["experience_sharing"]["per_recipient_multiplier"]["2"] == 0.65
    assert examples["normal_non_cannon_wave_before_25"]["base_last_hit_gold"] == 102
    assert examples["normal_non_cannon_wave_before_25"]["base_xp"] == 279
    assert examples["normal_non_cannon_wave_before_25"]["xp_received_per_nearby_champion"][
        "2"
    ] == pytest.approx(181.35)
    assert examples["cannon_wave_before_14"]["base_last_hit_gold"] == 152
    assert examples["cannon_wave_before_14"]["base_xp"] == 354
    assert examples["cannon_wave_from_14"]["base_last_hit_gold"] == 132
    assert examples["every_wave_from_30"]["base_last_hit_gold"] == 118
    assert examples["every_wave_from_30"]["base_xp"] == 261
    assert all(
        entry["classification"] == "modelled opportunity, not observed receipt"
        for entry in examples.values()
    )
    assert all(source.startswith("https://") for source in knowledge["sources"])


def test_economy_fundamentals_include_passive_gold_roles_and_allocations() -> None:
    result = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="economy", patch="26.15")
    )
    knowledge = result["knowledge"]

    assert knowledge["passive_gold"]["starts_at_seconds"] == 65
    assert knowledge["passive_gold"]["rate_gold_per_second"] == 2.04
    assert knowledge["role_modifiers"]["top_quest_completed"]["non_champion_xp_multiplier"] == 1.11
    assert knowledge["role_modifiers"]["bottom_quest_completed"] == {
        "one_time_gold": 300,
        "bonus_gold_per_minion_kill": 2,
    }
    assert knowledge["neutral_objectives"]["three_void_grubs"]["base_gold_total"] == 90
    assert (
        knowledge["neutral_objectives"]["three_void_grubs"]["raw_local_xp_total_before_sharing"]
        == 195
    )
    assert (
        "not 90 gold per teammate"
        in knowledge["neutral_objectives"]["three_void_grubs"]["allocation_warning"]
    )
    assert knowledge["analysis_model"]["separation"] == {
        "observed": "Riot Match V5 totals, frames, and events only.",
        "derived": "Arithmetic computed solely from observed fields.",
        "modelled": "Patch rules plus explicit collection, proximity, sharing, and wave assumptions.",
    }


def test_economy_role_rules_are_patch_banded_within_2026() -> None:
    patch_26_6 = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="economy", patch="26.6")
    )["knowledge"]
    patch_26_8 = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="economy", patch="26.8")
    )["knowledge"]

    assert (
        patch_26_6["role_modifiers"]["top_quest_completed"]["non_champion_xp_multiplier"] == 1.125
    )
    assert patch_26_6["role_modifiers"]["support_excess_minion_penalty"]["status"] == (
        "present_but_not_quantified_here"
    )
    assert patch_26_8["role_modifiers"]["support_excess_minion_penalty"]["status"] == "removed"


def test_economy_refuses_numeric_models_outside_verified_patch_band() -> None:
    knowledge = LolAnalysisService(ClientDouble()).knowledge(
        LolKnowledgeRequest(topic="minions", patch="25.24")
    )["knowledge"]

    assert knowledge["patch_identity"]["model_status"] == "unavailable"
    assert "minion_units" not in knowledge
    assert "26.1 through 26.15" in knowledge["unavailable_reason"]


def test_structure_and_item_efficiency_fundamentals_are_explicit() -> None:
    service = LolAnalysisService(ClientDouble())
    structures = service.knowledge(LolKnowledgeRequest(topic="structures", patch="26.15"))[
        "knowledge"
    ]
    efficiency = service.knowledge(LolKnowledgeRequest(topic="item_efficiency", patch="26.15"))[
        "knowledge"
    ]

    assert structures["structures"]["outer_turret"]["five_plate_local_gold_range"] == [
        400,
        600,
    ]
    assert structures["structures"]["first_turret_bonus"]["local_shared_gold"] == 300
    assert efficiency["baseline_component_ids"]["attack_damage"] == 1036
    assert "riot_lol_item_economy" in " ".join(efficiency["method"])
    assert (
        "never be described as total item value" in " ".join(efficiency["limitations"]).casefold()
    )


@pytest.mark.asyncio
async def test_item_economy_can_use_explicit_patch_or_match_patch() -> None:
    client = ClientDouble()
    service = LolAnalysisService(client)

    explicit = await service.item_economy(
        LolItemEconomyRequest(item_name="Synthetic Blade", patch="26.15")
    )
    match_based = await service.item_economy(
        LolItemEconomyRequest(item_id=3078, match_id="EUW1_9001")
    )

    assert explicit["match_basis"] is None
    assert explicit["economy"]["item"]["name"] == "Synthetic Blade"
    assert match_based["match_basis"] == {
        "match_id": "EUW1_9001",
        "route": "europe",
        "game_version": "14.10.321.1234",
        "queue_id": 420,
        "map_id": 11,
        "game_mode": "CLASSIC",
    }
    assert explicit["applicability"]["status"] == "standard_summoners_rift_assumed"
    assert match_based["applicability"]["status"] == "standard_summoners_rift"
    efficiency_calls = [call for call in client.static.calls if call[0] == "get_item_efficiency"]
    assert efficiency_calls[0][1]["game_version"] == "26.15"
    assert efficiency_calls[1][1]["game_version"] == "14.10.321.1234"


@pytest.mark.asyncio
async def test_item_economy_flags_alternate_queue_modifiers() -> None:
    match = make_match(game_version="16.15.1")
    match["info"]["queueId"] = 480
    client = ClientDouble(matches={"EUW1_9001": match})

    result = await LolAnalysisService(client).item_economy(
        LolItemEconomyRequest(item_id=3078, match_id="EUW1_9001")
    )

    assert result["applicability"]["status"] == "unverified_mode"
    assert "not included" in result["applicability"]["warning"]
