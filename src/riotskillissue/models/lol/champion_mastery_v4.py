from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChampionMastery(BaseModel):
    "This object contains single Champion Mastery information for player and champion…"

    champion_id: int = Field(
        alias="championId",
        description="Champion ID for this entry.",
    )
    champion_level: int = Field(
        alias="championLevel",
        description="".join(("Champion level for specified player and champi", "on combination.")),
    )
    champion_points: int = Field(
        alias="championPoints",
        description="".join(
            (
                "Total number of champion points for this playe",
                "r and champion combination - they are used to ",
                "determine championLevel.",
            )
        ),
    )
    champion_points_since_last_level: int = Field(
        alias="championPointsSinceLastLevel",
        description="".join(("Number of points earned since current level ha", "s been achieved.")),
    )
    champion_points_until_next_level: int = Field(
        alias="championPointsUntilNextLevel",
        description="".join(
            (
                "Number of points needed to achieve next level.",
                " Zero if player reached maximum champion level",
                " for this champion.",
            )
        ),
    )
    champion_season_milestone: int = Field(
        alias="championSeasonMilestone",
    )
    chest_granted: Optional[bool] = Field(
        default=None,
        alias="chestGranted",
        description="".join(("Is chest granted for this champion or not in c", "urrent season.")),
    )
    last_play_time: int = Field(
        alias="lastPlayTime",
        description="".join(
            (
                "Last time this champion was played by this pla",
                "yer - in Unix milliseconds time format.",
            )
        ),
    )
    mark_required_for_next_level: int = Field(
        alias="markRequiredForNextLevel",
    )
    milestone_grades: Optional[List[str]] = Field(
        default=None,
        alias="milestoneGrades",
    )
    next_season_milestone: NextSeasonMilestones = Field(
        alias="nextSeasonMilestone",
    )
    puuid: str = Field(
        alias="puuid",
        description="".join(
            ("Player Universal Unique Identifier. Exact leng", "th of 78 characters. (Encrypted)")
        ),
    )
    tokens_earned: int = Field(
        alias="tokensEarned",
        description="".join(
            (
                "The token earned for this champion at the curr",
                "ent championLevel. When the championLevel is a",
                "dvanced the tokensEarned resets to 0.",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class NextSeasonMilestones(BaseModel):
    "This object contains required next season milestone information."

    bonus: bool = Field(
        alias="bonus",
        description="Bonus.",
    )
    require_grade_counts: Dict[str, int] = Field(
        alias="requireGradeCounts",
    )
    reward_config: Optional[RewardConfig] = Field(
        default=None,
        alias="rewardConfig",
        description="Reward configuration.",
    )
    reward_marks: int = Field(
        alias="rewardMarks",
        description="Reward marks.",
    )
    total_games_requires: int = Field(
        alias="totalGamesRequires",
    )

    model_config = ConfigDict(populate_by_name=True)


class RewardConfig(BaseModel):
    "This object contains required reward config information."

    maximum_reward: int = Field(
        alias="maximumReward",
        description="Maximun reward",
    )
    reward_type: str = Field(
        alias="rewardType",
        description="Reward type",
    )
    reward_value: str = Field(
        alias="rewardValue",
        description="Reward value",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    ChampionMastery,
    NextSeasonMilestones,
    RewardConfig,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type
