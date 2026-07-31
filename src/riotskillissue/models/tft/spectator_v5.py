from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BannedChampion(BaseModel):
    champion_id: int = Field(
        alias="championId",
        description="The ID of the banned champion",
    )
    pick_turn: int = Field(
        alias="pickTurn",
        description="The turn during which the champion was banned",
    )
    team_id: int = Field(
        alias="teamId",
        description="The ID of the team that banned the champion",
    )

    model_config = ConfigDict(populate_by_name=True)


class CurrentGameInfo(BaseModel):
    banned_champions: List[BannedChampion] = Field(
        alias="bannedChampions",
        description="Banned champion information",
    )
    game_id: int = Field(
        alias="gameId",
        description="The ID of the game",
    )
    game_length: int = Field(
        alias="gameLength",
        description="".join(
            ("The amount of time in seconds that has passed ", "since the game started")
        ),
    )
    game_mode: str = Field(
        alias="gameMode",
        description="The game mode",
    )
    game_queue_config_id: Optional[int] = Field(
        default=None,
        alias="gameQueueConfigId",
        description="".join(
            ("The queue type (queue types are documented on ", "the Game Constants page)")
        ),
    )
    game_start_time: int = Field(
        alias="gameStartTime",
        description="".join(("The game start time represented in epoch milli", "seconds")),
    )
    game_type: str = Field(
        alias="gameType",
        description="The game type",
    )
    map_id: int = Field(
        alias="mapId",
        description="The ID of the map",
    )
    observers: Observer = Field(
        alias="observers",
        description="The observer information",
    )
    participants: List[CurrentGameParticipant] = Field(
        alias="participants",
        description="The participant information",
    )
    platform_id: str = Field(
        alias="platformId",
        description="".join(("The ID of the platform on which the game is be", "ing played")),
    )

    model_config = ConfigDict(populate_by_name=True)


class CurrentGameParticipant(BaseModel):
    champion_id: int = Field(
        alias="championId",
        description="".join(("The ID of the champion played by this particip", "ant")),
    )
    game_customization_objects: List[GameCustomizationObject] = Field(
        alias="gameCustomizationObjects",
        description="List of Game Customizations",
    )
    perks: Optional[Perks] = Field(
        default=None,
        alias="perks",
        description="Perks/Runes Reforged Information",
    )
    profile_icon_id: int = Field(
        alias="profileIconId",
        description="".join(("The ID of the profile icon used by this partic", "ipant")),
    )
    puuid: Optional[str] = Field(
        default=None,
        alias="puuid",
        description="".join(
            ("The encrypted puuid of this participant. null ", "when the player is anonym.")
        ),
    )
    riot_id: Optional[str] = Field(
        default=None,
        alias="riotId",
    )
    spell1_id: int = Field(
        alias="spell1Id",
        description="".join(("The ID of the first summoner spell used by thi", "s participant")),
    )
    spell2_id: int = Field(
        alias="spell2Id",
        description="".join(("The ID of the second summoner spell used by th", "is participant")),
    )
    team_id: int = Field(
        alias="teamId",
        description="".join(
            ("The team ID of this participant, indicating th", "e participant's team")
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class GameCustomizationObject(BaseModel):
    category: str = Field(
        alias="category",
        description="Category identifier for Game Customization",
    )
    content: str = Field(
        alias="content",
        description="Game Customization content",
    )

    model_config = ConfigDict(populate_by_name=True)


class Observer(BaseModel):
    encryption_key: str = Field(
        alias="encryptionKey",
        description="".join(("Key used to decrypt the spectator grid game da", "ta for playback")),
    )

    model_config = ConfigDict(populate_by_name=True)


class Perks(BaseModel):
    perk_ids: List[int] = Field(
        alias="perkIds",
        description="IDs of the perks/runes assigned.",
    )
    perk_style: int = Field(
        alias="perkStyle",
        description="Primary runes path",
    )
    perk_sub_style: int = Field(
        alias="perkSubStyle",
        description="Secondary runes path",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    BannedChampion,
    CurrentGameInfo,
    CurrentGameParticipant,
    GameCustomizationObject,
    Observer,
    Perks,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type
