from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Ban(BaseModel):
    champion_id: int = Field(
        alias="championId",
    )
    pick_turn: int = Field(
        alias="pickTurn",
    )

    model_config = ConfigDict(populate_by_name=True)


class Challenges(BaseModel):
    "Challenges DTO"

    param_12_assist_streak_count: Optional[int] = Field(
        default=None,
        alias="12AssistStreakCount",
    )
    heal_from_map_sources: Optional[float] = Field(
        default=None,
        alias="HealFromMapSources",
    )
    infernal_scale_pickup: Optional[int] = Field(
        default=None,
        alias="InfernalScalePickup",
    )
    swarm__defeat_aatrox: Optional[int] = Field(
        default=None,
        alias="SWARM_DefeatAatrox",
    )
    swarm__defeat_briar: Optional[int] = Field(
        default=None,
        alias="SWARM_DefeatBriar",
    )
    swarm__defeat_mini_bosses: Optional[int] = Field(
        default=None,
        alias="SWARM_DefeatMiniBosses",
    )
    swarm__evolve_weapon: Optional[int] = Field(
        default=None,
        alias="SWARM_EvolveWeapon",
    )
    swarm__have3_passives: Optional[int] = Field(
        default=None,
        alias="SWARM_Have3Passives",
    )
    swarm__kill_enemy: Optional[int] = Field(
        default=None,
        alias="SWARM_KillEnemy",
    )
    swarm__pickup_gold: Optional[float] = Field(
        default=None,
        alias="SWARM_PickupGold",
    )
    swarm__reach_level50: Optional[int] = Field(
        default=None,
        alias="SWARM_ReachLevel50",
    )
    swarm__survive15_min: Optional[int] = Field(
        default=None,
        alias="SWARM_Survive15Min",
    )
    swarm__win_with5_evolved_weapons: Optional[int] = Field(
        default=None,
        alias="SWARM_WinWith5EvolvedWeapons",
    )
    ability_uses: Optional[int] = Field(
        default=None,
        alias="abilityUses",
    )
    aces_before15_minutes: Optional[int] = Field(
        default=None,
        alias="acesBefore15Minutes",
    )
    allied_jungle_monster_kills: Optional[float] = Field(
        default=None,
        alias="alliedJungleMonsterKills",
    )
    baron_buff_gold_advantage_over_threshold: Optional[int] = Field(
        default=None,
        alias="baronBuffGoldAdvantageOverThreshold",
    )
    baron_takedowns: Optional[int] = Field(
        default=None,
        alias="baronTakedowns",
    )
    blast_cone_opposite_opponent_count: Optional[int] = Field(
        default=None,
        alias="blastConeOppositeOpponentCount",
    )
    bounty_gold: Optional[float] = Field(
        default=None,
        alias="bountyGold",
    )
    buffs_stolen: Optional[int] = Field(
        default=None,
        alias="buffsStolen",
    )
    complete_support_quest_in_time: Optional[int] = Field(
        default=None,
        alias="completeSupportQuestInTime",
    )
    control_ward_time_coverage_in_river_or_enemy_half: Optional[float] = Field(
        default=None,
        alias="controlWardTimeCoverageInRiverOrEnemyHalf",
    )
    control_wards_placed: Optional[int] = Field(
        default=None,
        alias="controlWardsPlaced",
    )
    damage_per_minute: Optional[float] = Field(
        default=None,
        alias="damagePerMinute",
    )
    damage_taken_on_team_percentage: Optional[float] = Field(
        default=None,
        alias="damageTakenOnTeamPercentage",
    )
    danced_with_rift_herald: Optional[int] = Field(
        default=None,
        alias="dancedWithRiftHerald",
    )
    deaths_by_enemy_champs: Optional[int] = Field(
        default=None,
        alias="deathsByEnemyChamps",
    )
    dodge_skill_shots_small_window: Optional[int] = Field(
        default=None,
        alias="dodgeSkillShotsSmallWindow",
    )
    double_aces: Optional[int] = Field(
        default=None,
        alias="doubleAces",
    )
    dragon_takedowns: Optional[int] = Field(
        default=None,
        alias="dragonTakedowns",
    )
    earliest_baron: Optional[float] = Field(
        default=None,
        alias="earliestBaron",
    )
    earliest_dragon_takedown: Optional[float] = Field(
        default=None,
        alias="earliestDragonTakedown",
    )
    earliest_elder_dragon: Optional[float] = Field(
        default=None,
        alias="earliestElderDragon",
    )
    early_laning_phase_gold_exp_advantage: Optional[float] = Field(
        default=None,
        alias="earlyLaningPhaseGoldExpAdvantage",
    )
    effective_heal_and_shielding: Optional[float] = Field(
        default=None,
        alias="effectiveHealAndShielding",
    )
    elder_dragon_kills_with_opposing_soul: Optional[int] = Field(
        default=None,
        alias="elderDragonKillsWithOpposingSoul",
    )
    elder_dragon_multikills: Optional[int] = Field(
        default=None,
        alias="elderDragonMultikills",
    )
    enemy_champion_immobilizations: Optional[int] = Field(
        default=None,
        alias="enemyChampionImmobilizations",
    )
    enemy_jungle_monster_kills: Optional[float] = Field(
        default=None,
        alias="enemyJungleMonsterKills",
    )
    epic_monster_kills_near_enemy_jungler: Optional[int] = Field(
        default=None,
        alias="epicMonsterKillsNearEnemyJungler",
    )
    epic_monster_kills_within30_seconds_of_spawn: Optional[int] = Field(
        default=None,
        alias="epicMonsterKillsWithin30SecondsOfSpawn",
    )
    epic_monster_steals: Optional[int] = Field(
        default=None,
        alias="epicMonsterSteals",
    )
    epic_monster_stolen_without_smite: Optional[int] = Field(
        default=None,
        alias="epicMonsterStolenWithoutSmite",
    )
    faster_support_quest_completion: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="fasterSupportQuestCompletion",
    )
    fastest_legendary: Optional[float] = Field(
        default=None,
        alias="fastestLegendary",
    )
    first_turret_killed: Optional[float] = Field(
        default=None,
        alias="firstTurretKilled",
    )
    first_turret_killed_time: Optional[float] = Field(
        default=None,
        alias="firstTurretKilledTime",
    )
    fist_bump_participation: Optional[int] = Field(
        default=None,
        alias="fistBumpParticipation",
    )
    flawless_aces: Optional[int] = Field(
        default=None,
        alias="flawlessAces",
    )
    full_team_takedown: Optional[int] = Field(
        default=None,
        alias="fullTeamTakedown",
    )
    game_length: Optional[float] = Field(
        default=None,
        alias="gameLength",
    )
    get_takedowns_in_all_lanes_early_jungle_as_laner: Optional[int] = Field(
        default=None,
        alias="getTakedownsInAllLanesEarlyJungleAsLaner",
    )
    gold_per_minute: Optional[float] = Field(
        default=None,
        alias="goldPerMinute",
    )
    had_afk_teammate: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="hadAfkTeammate",
    )
    had_open_nexus: Optional[int] = Field(
        default=None,
        alias="hadOpenNexus",
    )
    highest_champion_damage: Optional[int] = Field(
        default=None,
        alias="highestChampionDamage",
    )
    highest_crowd_control_score: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="highestCrowdControlScore",
    )
    highest_ward_kills: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="highestWardKills",
    )
    immobilize_and_kill_with_ally: Optional[int] = Field(
        default=None,
        alias="immobilizeAndKillWithAlly",
    )
    initial_buff_count: Optional[int] = Field(
        default=None,
        alias="initialBuffCount",
    )
    initial_crab_count: Optional[int] = Field(
        default=None,
        alias="initialCrabCount",
    )
    jungle_cs_before10_minutes: Optional[float] = Field(
        default=None,
        alias="jungleCsBefore10Minutes",
    )
    jungler_kills_early_jungle: Optional[int] = Field(
        default=None,
        alias="junglerKillsEarlyJungle",
    )
    jungler_takedowns_near_damaged_epic_monster: Optional[int] = Field(
        default=None,
        alias="junglerTakedownsNearDamagedEpicMonster",
    )
    k_turrets_destroyed_before_plates_fall: Optional[int] = Field(
        default=None,
        alias="kTurretsDestroyedBeforePlatesFall",
    )
    kda: Optional[float] = Field(
        default=None,
        alias="kda",
    )
    kill_after_hidden_with_ally: Optional[int] = Field(
        default=None,
        alias="killAfterHiddenWithAlly",
    )
    kill_participation: Optional[float] = Field(
        default=None,
        alias="killParticipation",
    )
    killed_champ_took_full_team_damage_survived: Optional[int] = Field(
        default=None,
        alias="killedChampTookFullTeamDamageSurvived",
    )
    killing_sprees: Optional[int] = Field(
        default=None,
        alias="killingSprees",
    )
    kills_near_enemy_turret: Optional[int] = Field(
        default=None,
        alias="killsNearEnemyTurret",
    )
    kills_on_laners_early_jungle_as_jungler: Optional[int] = Field(
        default=None,
        alias="killsOnLanersEarlyJungleAsJungler",
    )
    kills_on_other_lanes_early_jungle_as_laner: Optional[int] = Field(
        default=None,
        alias="killsOnOtherLanesEarlyJungleAsLaner",
    )
    kills_on_recently_healed_by_aram_pack: Optional[int] = Field(
        default=None,
        alias="killsOnRecentlyHealedByAramPack",
    )
    kills_under_own_turret: Optional[int] = Field(
        default=None,
        alias="killsUnderOwnTurret",
    )
    kills_with_help_from_epic_monster: Optional[int] = Field(
        default=None,
        alias="killsWithHelpFromEpicMonster",
    )
    knock_enemy_into_team_and_kill: Optional[int] = Field(
        default=None,
        alias="knockEnemyIntoTeamAndKill",
    )
    land_skill_shots_early_game: Optional[int] = Field(
        default=None,
        alias="landSkillShotsEarlyGame",
    )
    lane_minions_first10_minutes: Optional[int] = Field(
        default=None,
        alias="laneMinionsFirst10Minutes",
    )
    laning_phase_gold_exp_advantage: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="laningPhaseGoldExpAdvantage",
    )
    legendary_count: Optional[int] = Field(
        default=None,
        alias="legendaryCount",
    )
    legendary_item_used: Optional[List[int]] = Field(
        default=None,
        alias="legendaryItemUsed",
    )
    lost_an_inhibitor: Optional[int] = Field(
        default=None,
        alias="lostAnInhibitor",
    )
    max_cs_advantage_on_lane_opponent: Optional[float] = Field(
        default=None,
        alias="maxCsAdvantageOnLaneOpponent",
    )
    max_kill_deficit: Optional[int] = Field(
        default=None,
        alias="maxKillDeficit",
    )
    max_level_lead_lane_opponent: Optional[int] = Field(
        default=None,
        alias="maxLevelLeadLaneOpponent",
    )
    mejais_full_stack_in_time: Optional[int] = Field(
        default=None,
        alias="mejaisFullStackInTime",
    )
    more_enemy_jungle_than_opponent: Optional[float] = Field(
        default=None,
        alias="moreEnemyJungleThanOpponent",
    )
    most_wards_destroyed_one_sweeper: Optional[int] = Field(
        default=None,
        alias="mostWardsDestroyedOneSweeper",
    )
    multi_kill_one_spell: Optional[int] = Field(
        default=None,
        alias="multiKillOneSpell",
        description="".join(
            (
                "This is an offshoot of the OneStone challenge.",
                " The code checks if a spell with the same inst",
                "ance ID does the final point of damage to at l",
                "east 2 Champions. It doesn't matter if they're",
                " enemies, but you cannot hurt your friends.",
            )
        ),
    )
    multi_turret_rift_herald_count: Optional[int] = Field(
        default=None,
        alias="multiTurretRiftHeraldCount",
    )
    multikills: Optional[int] = Field(
        default=None,
        alias="multikills",
    )
    multikills_after_aggressive_flash: Optional[int] = Field(
        default=None,
        alias="multikillsAfterAggressiveFlash",
    )
    mythic_item_used: Optional[int] = Field(
        default=None,
        alias="mythicItemUsed",
    )
    outer_turret_executes_before10_minutes: Optional[int] = Field(
        default=None,
        alias="outerTurretExecutesBefore10Minutes",
    )
    outnumbered_kills: Optional[int] = Field(
        default=None,
        alias="outnumberedKills",
    )
    outnumbered_nexus_kill: Optional[int] = Field(
        default=None,
        alias="outnumberedNexusKill",
    )
    perfect_dragon_souls_taken: Optional[int] = Field(
        default=None,
        alias="perfectDragonSoulsTaken",
    )
    perfect_game: Optional[int] = Field(
        default=None,
        alias="perfectGame",
    )
    pick_kill_with_ally: Optional[int] = Field(
        default=None,
        alias="pickKillWithAlly",
    )
    played_champ_select_position: Optional[Literal[0, 1]] = Field(
        default=None,
        alias="playedChampSelectPosition",
    )
    poro_explosions: Optional[int] = Field(
        default=None,
        alias="poroExplosions",
    )
    quick_cleanse: Optional[int] = Field(
        default=None,
        alias="quickCleanse",
    )
    quick_first_turret: Optional[int] = Field(
        default=None,
        alias="quickFirstTurret",
    )
    quick_solo_kills: Optional[int] = Field(
        default=None,
        alias="quickSoloKills",
    )
    rift_herald_takedowns: Optional[int] = Field(
        default=None,
        alias="riftHeraldTakedowns",
    )
    save_ally_from_death: Optional[int] = Field(
        default=None,
        alias="saveAllyFromDeath",
    )
    scuttle_crab_kills: Optional[int] = Field(
        default=None,
        alias="scuttleCrabKills",
    )
    shortest_time_to_ace_from_first_takedown: Optional[float] = Field(
        default=None,
        alias="shortestTimeToAceFromFirstTakedown",
    )
    skillshots_dodged: Optional[int] = Field(
        default=None,
        alias="skillshotsDodged",
    )
    skillshots_hit: Optional[int] = Field(
        default=None,
        alias="skillshotsHit",
    )
    snowballs_hit: Optional[int] = Field(
        default=None,
        alias="snowballsHit",
    )
    solo_baron_kills: Optional[int] = Field(
        default=None,
        alias="soloBaronKills",
    )
    solo_kills: Optional[int] = Field(
        default=None,
        alias="soloKills",
    )
    solo_turrets_lategame: Optional[int] = Field(
        default=None,
        alias="soloTurretsLategame",
    )
    stealth_wards_placed: Optional[int] = Field(
        default=None,
        alias="stealthWardsPlaced",
    )
    survived_single_digit_hp_count: Optional[int] = Field(
        default=None,
        alias="survivedSingleDigitHpCount",
    )
    survived_three_immobilizes_in_fight: Optional[int] = Field(
        default=None,
        alias="survivedThreeImmobilizesInFight",
    )
    takedown_on_first_turret: Optional[int] = Field(
        default=None,
        alias="takedownOnFirstTurret",
    )
    takedowns: Optional[int] = Field(
        default=None,
        alias="takedowns",
    )
    takedowns_after_gaining_level_advantage: Optional[int] = Field(
        default=None,
        alias="takedownsAfterGainingLevelAdvantage",
    )
    takedowns_before_jungle_minion_spawn: Optional[int] = Field(
        default=None,
        alias="takedownsBeforeJungleMinionSpawn",
    )
    takedowns_first25_minutes: Optional[int] = Field(
        default=None,
        alias="takedownsFirst25Minutes",
    )
    takedowns_first_x_minutes: Optional[int] = Field(
        default=None,
        alias="takedownsFirstXMinutes",
    )
    takedowns_in_alcove: Optional[int] = Field(
        default=None,
        alias="takedownsInAlcove",
    )
    takedowns_in_enemy_fountain: Optional[int] = Field(
        default=None,
        alias="takedownsInEnemyFountain",
    )
    team_baron_kills: Optional[int] = Field(
        default=None,
        alias="teamBaronKills",
    )
    team_damage_percentage: Optional[float] = Field(
        default=None,
        alias="teamDamagePercentage",
    )
    team_elder_dragon_kills: Optional[int] = Field(
        default=None,
        alias="teamElderDragonKills",
    )
    team_rift_herald_kills: Optional[int] = Field(
        default=None,
        alias="teamRiftHeraldKills",
    )
    teleport_takedowns: Optional[int] = Field(
        default=None,
        alias="teleportTakedowns",
    )
    third_inhibitor_destroyed_time: Optional[float] = Field(
        default=None,
        alias="thirdInhibitorDestroyedTime",
    )
    three_wards_one_sweeper_count: Optional[int] = Field(
        default=None,
        alias="threeWardsOneSweeperCount",
    )
    took_large_damage_survived: Optional[int] = Field(
        default=None,
        alias="tookLargeDamageSurvived",
    )
    turret_plates_taken: Optional[int] = Field(
        default=None,
        alias="turretPlatesTaken",
    )
    turret_takedowns: Optional[int] = Field(
        default=None,
        alias="turretTakedowns",
    )
    turrets_taken_with_rift_herald: Optional[int] = Field(
        default=None,
        alias="turretsTakenWithRiftHerald",
        description="".join(
            (
                "Any player who damages a tower that is destroy",
                "ed within 30 seconds of a Rift Herald charge w",
                "ill receive credit. A player who does not dama",
                "ge the tower will not receive credit.",
            )
        ),
    )
    twenty_minions_in3_seconds_count: Optional[int] = Field(
        default=None,
        alias="twentyMinionsIn3SecondsCount",
    )
    two_wards_one_sweeper_count: Optional[int] = Field(
        default=None,
        alias="twoWardsOneSweeperCount",
    )
    unseen_recalls: Optional[int] = Field(
        default=None,
        alias="unseenRecalls",
    )
    vision_score_advantage_lane_opponent: Optional[float] = Field(
        default=None,
        alias="visionScoreAdvantageLaneOpponent",
    )
    vision_score_per_minute: Optional[float] = Field(
        default=None,
        alias="visionScorePerMinute",
    )
    void_monster_kill: Optional[int] = Field(
        default=None,
        alias="voidMonsterKill",
    )
    ward_takedowns: Optional[int] = Field(
        default=None,
        alias="wardTakedowns",
    )
    ward_takedowns_before20_m: Optional[int] = Field(
        default=None,
        alias="wardTakedownsBefore20M",
    )
    wards_guarded: Optional[int] = Field(
        default=None,
        alias="wardsGuarded",
    )

    model_config = ConfigDict(populate_by_name=True)


class ChampionStats(BaseModel):
    ability_haste: Optional[int] = Field(
        default=None,
        alias="abilityHaste",
    )
    ability_power: int = Field(
        alias="abilityPower",
    )
    armor: int = Field(
        alias="armor",
    )
    armor_pen: int = Field(
        alias="armorPen",
    )
    armor_pen_percent: int = Field(
        alias="armorPenPercent",
    )
    attack_damage: int = Field(
        alias="attackDamage",
    )
    attack_speed: int = Field(
        alias="attackSpeed",
    )
    bonus_armor_pen_percent: int = Field(
        alias="bonusArmorPenPercent",
    )
    bonus_magic_pen_percent: int = Field(
        alias="bonusMagicPenPercent",
    )
    cc_reduction: int = Field(
        alias="ccReduction",
    )
    cooldown_reduction: int = Field(
        alias="cooldownReduction",
    )
    health: int = Field(
        alias="health",
    )
    health_max: int = Field(
        alias="healthMax",
    )
    health_regen: int = Field(
        alias="healthRegen",
    )
    lifesteal: int = Field(
        alias="lifesteal",
    )
    magic_pen: int = Field(
        alias="magicPen",
    )
    magic_pen_percent: int = Field(
        alias="magicPenPercent",
    )
    magic_resist: int = Field(
        alias="magicResist",
    )
    movement_speed: int = Field(
        alias="movementSpeed",
    )
    omnivamp: Optional[int] = Field(
        default=None,
        alias="omnivamp",
    )
    physical_vamp: Optional[int] = Field(
        default=None,
        alias="physicalVamp",
    )
    power: int = Field(
        alias="power",
    )
    power_max: int = Field(
        alias="powerMax",
    )
    power_regen: int = Field(
        alias="powerRegen",
    )
    spell_vamp: int = Field(
        alias="spellVamp",
    )

    model_config = ConfigDict(populate_by_name=True)


class DamageStats(BaseModel):
    magic_damage_done: int = Field(
        alias="magicDamageDone",
    )
    magic_damage_done_to_champions: int = Field(
        alias="magicDamageDoneToChampions",
    )
    magic_damage_taken: int = Field(
        alias="magicDamageTaken",
    )
    physical_damage_done: int = Field(
        alias="physicalDamageDone",
    )
    physical_damage_done_to_champions: int = Field(
        alias="physicalDamageDoneToChampions",
    )
    physical_damage_taken: int = Field(
        alias="physicalDamageTaken",
    )
    total_damage_done: int = Field(
        alias="totalDamageDone",
    )
    total_damage_done_to_champions: int = Field(
        alias="totalDamageDoneToChampions",
    )
    total_damage_taken: int = Field(
        alias="totalDamageTaken",
    )
    true_damage_done: int = Field(
        alias="trueDamageDone",
    )
    true_damage_done_to_champions: int = Field(
        alias="trueDamageDoneToChampions",
    )
    true_damage_taken: int = Field(
        alias="trueDamageTaken",
    )

    model_config = ConfigDict(populate_by_name=True)


class EventsTimeLine(BaseModel):
    actual_start_time: Optional[int] = Field(
        default=None,
        alias="actualStartTime",
    )
    after_id: Optional[int] = Field(
        default=None,
        alias="afterId",
    )
    assisting_participant_ids: Optional[List[int]] = Field(
        default=None,
        alias="assistingParticipantIds",
    )
    before_id: Optional[int] = Field(
        default=None,
        alias="beforeId",
    )
    bounty: Optional[int] = Field(
        default=None,
        alias="bounty",
    )
    building_type: Optional[str] = Field(
        default=None,
        alias="buildingType",
    )
    creator_id: Optional[int] = Field(
        default=None,
        alias="creatorId",
    )
    feat_type: Optional[int] = Field(
        default=None,
        alias="featType",
    )
    feat_value: Optional[int] = Field(
        default=None,
        alias="featValue",
    )
    game_id: Optional[int] = Field(
        default=None,
        alias="gameId",
    )
    gold_gain: Optional[int] = Field(
        default=None,
        alias="goldGain",
    )
    item_id: Optional[int] = Field(
        default=None,
        alias="itemId",
    )
    kill_streak_length: Optional[int] = Field(
        default=None,
        alias="killStreakLength",
    )
    kill_type: Optional[str] = Field(
        default=None,
        alias="killType",
    )
    killer_id: Optional[int] = Field(
        default=None,
        alias="killerId",
    )
    killer_team_id: Optional[int] = Field(
        default=None,
        alias="killerTeamId",
    )
    lane_type: Optional[str] = Field(
        default=None,
        alias="laneType",
    )
    level: Optional[int] = Field(
        default=None,
        alias="level",
    )
    level_up_type: Optional[str] = Field(
        default=None,
        alias="levelUpType",
    )
    monster_sub_type: Optional[str] = Field(
        default=None,
        alias="monsterSubType",
    )
    monster_type: Optional[str] = Field(
        default=None,
        alias="monsterType",
    )
    multi_kill_length: Optional[int] = Field(
        default=None,
        alias="multiKillLength",
    )
    name: Optional[str] = Field(
        default=None,
        alias="name",
    )
    participant_id: Optional[int] = Field(
        default=None,
        alias="participantId",
    )
    position: Optional[Position] = Field(
        default=None,
        alias="position",
    )
    real_timestamp: Optional[int] = Field(
        default=None,
        alias="realTimestamp",
    )
    shutdown_bounty: Optional[int] = Field(
        default=None,
        alias="shutdownBounty",
    )
    skill_slot: Optional[int] = Field(
        default=None,
        alias="skillSlot",
    )
    team_id: Optional[int] = Field(
        default=None,
        alias="teamId",
    )
    timestamp: int = Field(
        alias="timestamp",
    )
    tower_type: Optional[str] = Field(
        default=None,
        alias="towerType",
    )
    transform_type: Optional[str] = Field(
        default=None,
        alias="transformType",
    )
    type: str = Field(
        alias="type",
    )
    victim_damage_dealt: Optional[List[MatchTimelineVictimDamage]] = Field(
        default=None,
        alias="victimDamageDealt",
    )
    victim_damage_received: Optional[List[MatchTimelineVictimDamage]] = Field(
        default=None,
        alias="victimDamageReceived",
    )
    victim_id: Optional[int] = Field(
        default=None,
        alias="victimId",
    )
    victim_teamfight_damage_dealt: Optional[List[MatchTimelineVictimDamage]] = Field(
        default=None,
        alias="victimTeamfightDamageDealt",
    )
    victim_teamfight_damage_received: Optional[List[MatchTimelineVictimDamage]] = Field(
        default=None,
        alias="victimTeamfightDamageReceived",
    )
    ward_type: Optional[str] = Field(
        default=None,
        alias="wardType",
    )
    winning_team: Optional[int] = Field(
        default=None,
        alias="winningTeam",
    )

    model_config = ConfigDict(populate_by_name=True)


class Feat(BaseModel):
    feat_state: Optional[int] = Field(
        default=None,
        alias="featState",
    )

    model_config = ConfigDict(populate_by_name=True)


class Feats(BaseModel):
    epic_monster_kill: Optional[Feat] = Field(
        default=None,
        alias="EPIC_MONSTER_KILL",
    )
    first_blood: Optional[Feat] = Field(
        default=None,
        alias="FIRST_BLOOD",
    )
    first_turret: Optional[Feat] = Field(
        default=None,
        alias="FIRST_TURRET",
    )

    model_config = ConfigDict(populate_by_name=True)


class FramesTimeLine(BaseModel):
    events: List[EventsTimeLine] = Field(
        alias="events",
    )
    participant_frames: Optional[Dict[str, ParticipantFrame]] = Field(
        default=None,
        alias="participantFrames",
    )
    timestamp: int = Field(
        alias="timestamp",
    )

    model_config = ConfigDict(populate_by_name=True)


class Info(BaseModel):
    end_of_game_result: Optional[str] = Field(
        default=None,
        alias="endOfGameResult",
        description="".join(("Refer to indicate if the game ended in termina", "tion.")),
    )
    game_creation: int = Field(
        alias="gameCreation",
        description="".join(
            (
                "Unix timestamp for when the game is created on",
                " the game server (i.e., the loading screen).",
            )
        ),
    )
    game_duration: int = Field(
        alias="gameDuration",
        description="".join(
            (
                "Prior to patch 11.20, this field returns the g",
                "ame length in milliseconds calculated from gam",
                "eEndTimestamp - gameStartTimestamp. Post patch",
                " 11.20, this field returns the max timePlayed ",
                "of any participant in the game in seconds, whi",
                "ch makes the behavior of this field consistent",
                " with that of match-v4. The best way to handli",
                "ng the change in this field is to treat the va",
                "lue as milliseconds if the gameEndTimestamp fi",
                "eld isn't in the response and to treat the val",
                "ue as seconds if gameEndTimestamp is in the re",
                "sponse.",
            )
        ),
    )
    game_end_timestamp: Optional[int] = Field(
        default=None,
        alias="gameEndTimestamp",
        description="".join(
            (
                "Unix timestamp for when match ends on the game",
                " server. This timestamp can occasionally be si",
                'gnificantly longer than when the match "ends".',
                " The most reliable way of determining the time",
                "stamp for the end of the match would be to add",
                " the max time played of any participant to the",
                " gameStartTimestamp. This field was added to m",
                "atch-v5 in patch 11.20 on Oct 5th, 2021.",
            )
        ),
    )
    game_id: int = Field(
        alias="gameId",
    )
    game_mode: str = Field(
        alias="gameMode",
        description="Refer to the Game Constants documentation.",
    )
    game_mode_mutators: Optional[List[str]] = Field(
        default=None,
        alias="gameModeMutators",
    )
    game_name: str = Field(
        alias="gameName",
    )
    game_start_timestamp: int = Field(
        alias="gameStartTimestamp",
        description="".join(("Unix timestamp for when match starts on the ga", "me server.")),
    )
    game_type: str = Field(
        alias="gameType",
    )
    game_version: str = Field(
        alias="gameVersion",
        description="".join(
            ("The first two parts can be used to determine t", "he patch a game was played on.")
        ),
    )
    map_id: int = Field(
        alias="mapId",
        description="Refer to the Game Constants documentation.",
    )
    participants: List[Participant] = Field(
        alias="participants",
    )
    platform_id: str = Field(
        alias="platformId",
        description="Platform where the match was played.",
    )
    queue_id: int = Field(
        alias="queueId",
        description="Refer to the Game Constants documentation.",
    )
    teams: List[Team] = Field(
        alias="teams",
    )
    tournament_code: Optional[str] = Field(
        default=None,
        alias="tournamentCode",
        description="".join(
            (
                "Tournament code used to generate the match. Th",
                "is field was added to match-v5 in patch 11.13 ",
                "on June 23rd, 2021.",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class InfoTimeLine(BaseModel):
    end_of_game_result: Optional[str] = Field(
        default=None,
        alias="endOfGameResult",
        description="".join(("Refer to indicate if the game ended in termina", "tion.")),
    )
    frame_interval: int = Field(
        alias="frameInterval",
    )
    frames: List[FramesTimeLine] = Field(
        alias="frames",
    )
    game_id: Optional[int] = Field(
        default=None,
        alias="gameId",
    )
    participants: Optional[List[ParticipantTimeLine]] = Field(
        default=None,
        alias="participants",
    )

    model_config = ConfigDict(populate_by_name=True)


class Match(BaseModel):
    info: Info = Field(
        alias="info",
        description="Match info.",
    )
    metadata: Metadata = Field(
        alias="metadata",
        description="Match metadata.",
    )

    model_config = ConfigDict(populate_by_name=True)


class MatchTimelineVictimDamage(BaseModel):
    basic: bool = Field(
        alias="basic",
    )
    magic_damage: int = Field(
        alias="magicDamage",
    )
    name: str = Field(
        alias="name",
    )
    participant_id: int = Field(
        alias="participantId",
    )
    physical_damage: int = Field(
        alias="physicalDamage",
    )
    spell_name: str = Field(
        alias="spellName",
    )
    spell_slot: int = Field(
        alias="spellSlot",
    )
    true_damage: int = Field(
        alias="trueDamage",
    )
    type: str = Field(
        alias="type",
    )

    model_config = ConfigDict(populate_by_name=True)


class Metadata(BaseModel):
    data_version: str = Field(
        alias="dataVersion",
        description="Match data version.",
    )
    match_id: str = Field(
        alias="matchId",
        description="Match id.",
    )
    participants: List[str] = Field(
        alias="participants",
        description="A list of participant PUUIDs.",
    )

    model_config = ConfigDict(populate_by_name=True)


class MetadataTimeLine(BaseModel):
    data_version: str = Field(
        alias="dataVersion",
        description="Match data version.",
    )
    match_id: str = Field(
        alias="matchId",
        description="Match id.",
    )
    participants: List[str] = Field(
        alias="participants",
        description="A list of participant PUUIDs.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Missions(BaseModel):
    "Missions DTO"

    player_score0: Optional[float] = Field(
        default=None,
        alias="playerScore0",
    )
    player_score1: Optional[float] = Field(
        default=None,
        alias="playerScore1",
    )
    player_score10: Optional[float] = Field(
        default=None,
        alias="playerScore10",
    )
    player_score11: Optional[float] = Field(
        default=None,
        alias="playerScore11",
    )
    player_score2: Optional[float] = Field(
        default=None,
        alias="playerScore2",
    )
    player_score3: Optional[float] = Field(
        default=None,
        alias="playerScore3",
    )
    player_score4: Optional[float] = Field(
        default=None,
        alias="playerScore4",
    )
    player_score5: Optional[float] = Field(
        default=None,
        alias="playerScore5",
    )
    player_score6: Optional[float] = Field(
        default=None,
        alias="playerScore6",
    )
    player_score7: Optional[float] = Field(
        default=None,
        alias="playerScore7",
    )
    player_score8: Optional[float] = Field(
        default=None,
        alias="playerScore8",
    )
    player_score9: Optional[float] = Field(
        default=None,
        alias="playerScore9",
    )

    model_config = ConfigDict(populate_by_name=True)


class Objective(BaseModel):
    first: bool = Field(
        alias="first",
    )
    kills: int = Field(
        alias="kills",
    )

    model_config = ConfigDict(populate_by_name=True)


class Objectives(BaseModel):
    atakhan: Optional[Objective] = Field(
        default=None,
        alias="atakhan",
    )
    baron: Objective = Field(
        alias="baron",
    )
    champion: Objective = Field(
        alias="champion",
    )
    dragon: Objective = Field(
        alias="dragon",
    )
    horde: Optional[Objective] = Field(
        default=None,
        alias="horde",
    )
    inhibitor: Objective = Field(
        alias="inhibitor",
    )
    rift_herald: Objective = Field(
        alias="riftHerald",
    )
    tower: Objective = Field(
        alias="tower",
    )

    model_config = ConfigDict(populate_by_name=True)


class Participant(BaseModel):
    player_behavior: Optional[ParticipantPlayerBehavior] = Field(
        default=None,
        alias="PlayerBehavior",
        description="".join(
            (
                "https://github.com/RiotGames/developer-relatio",
                "ns/issues/754#issuecomment-3940157820",
            )
        ),
    )
    all_in_pings: Optional[int] = Field(
        default=None,
        alias="allInPings",
        description="Yellow crossed swords",
    )
    assist_me_pings: Optional[int] = Field(
        default=None,
        alias="assistMePings",
        description="Green flag",
    )
    assists: int = Field(
        alias="assists",
    )
    bait_pings: Optional[int] = Field(
        default=None,
        alias="baitPings",
    )
    baron_kills: int = Field(
        alias="baronKills",
    )
    basic_pings: Optional[int] = Field(
        default=None,
        alias="basicPings",
        description="".join(("https://github.com/RiotGames/developer-relatio", "ns/issues/814")),
    )
    bounty_level: Optional[int] = Field(
        default=None,
        alias="bountyLevel",
    )
    caused_game_end_from_ignb_surrender: Optional[bool] = Field(
        default=None,
        alias="causedGameEndFromIGNBSurrender",
    )
    challenges: Optional[Challenges] = Field(
        default=None,
        alias="challenges",
    )
    champ_experience: int = Field(
        alias="champExperience",
    )
    champ_level: int = Field(
        alias="champLevel",
    )
    champion_id: int = Field(
        alias="championId",
        description="".join(
            (
                "Prior to patch 11.4, on Feb 18th, 2021, this f",
                "ield returned invalid championIds. We recommen",
                "d determining the champion based on the champi",
                "onName field for matches played prior to patch",
                " 11.4.",
            )
        ),
    )
    champion_name: str = Field(
        alias="championName",
    )
    champion_skin_id: Optional[int] = Field(
        default=None,
        alias="championSkinId",
    )
    champion_transform: int = Field(
        alias="championTransform",
        description="".join(
            (
                "This field is currently only utilized for Kayn",
                "'s transformations. (Legal values: 0 - None, 1",
                " - Slayer, 2 - Assassin)",
            )
        ),
    )
    command_pings: Optional[int] = Field(
        default=None,
        alias="commandPings",
        description="Blue generic ping (ALT+click)",
    )
    consumables_purchased: int = Field(
        alias="consumablesPurchased",
    )
    damage_dealt_to_buildings: Optional[int] = Field(
        default=None,
        alias="damageDealtToBuildings",
    )
    damage_dealt_to_epic_monsters: Optional[int] = Field(
        default=None,
        alias="damageDealtToEpicMonsters",
    )
    damage_dealt_to_objectives: int = Field(
        alias="damageDealtToObjectives",
    )
    damage_dealt_to_turrets: int = Field(
        alias="damageDealtToTurrets",
    )
    damage_self_mitigated: int = Field(
        alias="damageSelfMitigated",
    )
    danger_pings: Optional[int] = Field(
        default=None,
        alias="dangerPings",
        description="".join(("https://github.com/RiotGames/developer-relatio", "ns/issues/870")),
    )
    deaths: int = Field(
        alias="deaths",
    )
    detector_wards_placed: int = Field(
        alias="detectorWardsPlaced",
    )
    double_kills: int = Field(
        alias="doubleKills",
    )
    dragon_kills: int = Field(
        alias="dragonKills",
    )
    eligible_for_progression: Optional[bool] = Field(
        default=None,
        alias="eligibleForProgression",
    )
    enemy_missing_pings: Optional[int] = Field(
        default=None,
        alias="enemyMissingPings",
        description="Yellow questionmark",
    )
    enemy_vision_pings: Optional[int] = Field(
        default=None,
        alias="enemyVisionPings",
        description="Red eyeball",
    )
    first_blood_assist: bool = Field(
        alias="firstBloodAssist",
    )
    first_blood_kill: bool = Field(
        alias="firstBloodKill",
    )
    first_tower_assist: bool = Field(
        alias="firstTowerAssist",
    )
    first_tower_kill: bool = Field(
        alias="firstTowerKill",
    )
    game_ended_in_early_surrender: bool = Field(
        alias="gameEndedInEarlySurrender",
        description="".join(
            (
                "This is an offshoot of the OneStone challenge.",
                " The code checks if a spell with the same inst",
                "ance ID does the final point of damage to at l",
                "east 2 Champions. It doesn't matter if they're",
                " enemies, but you cannot hurt your friends.",
            )
        ),
    )
    game_ended_in_ignb_surrender: Optional[bool] = Field(
        default=None,
        alias="gameEndedInIGNBSurrender",
    )
    game_ended_in_surrender: bool = Field(
        alias="gameEndedInSurrender",
    )
    get_back_pings: Optional[int] = Field(
        default=None,
        alias="getBackPings",
        description="Yellow circle with horizontal line",
    )
    gold_earned: int = Field(
        alias="goldEarned",
    )
    gold_spent: int = Field(
        alias="goldSpent",
    )
    hold_pings: Optional[int] = Field(
        default=None,
        alias="holdPings",
    )
    individual_position: str = Field(
        alias="individualPosition",
        description="".join(
            (
                "Both individualPosition and teamPosition are c",
                "omputed by the game server and are different v",
                "ersions of the most likely position played by ",
                "a player. The individualPosition is the best g",
                "uess for which position the player actually pl",
                "ayed in isolation of anything else. The teamPo",
                "sition is the best guess for which position th",
                "e player actually played if we add the constra",
                "int that each team must have one top player, o",
                "ne jungle, one middle, etc. Generally the reco",
                "mmendation is to use the teamPosition field ov",
                "er the individualPosition field.",
            )
        ),
    )
    inhibitor_kills: int = Field(
        alias="inhibitorKills",
    )
    inhibitor_takedowns: Optional[int] = Field(
        default=None,
        alias="inhibitorTakedowns",
    )
    inhibitors_lost: Optional[int] = Field(
        default=None,
        alias="inhibitorsLost",
    )
    item0: int = Field(
        alias="item0",
    )
    item1: int = Field(
        alias="item1",
    )
    item2: int = Field(
        alias="item2",
    )
    item3: int = Field(
        alias="item3",
    )
    item4: int = Field(
        alias="item4",
    )
    item5: int = Field(
        alias="item5",
    )
    item6: int = Field(
        alias="item6",
    )
    items_purchased: int = Field(
        alias="itemsPurchased",
    )
    killing_sprees: int = Field(
        alias="killingSprees",
    )
    kills: int = Field(
        alias="kills",
    )
    lane: str = Field(
        alias="lane",
    )
    largest_critical_strike: int = Field(
        alias="largestCriticalStrike",
    )
    largest_killing_spree: int = Field(
        alias="largestKillingSpree",
    )
    largest_multi_kill: int = Field(
        alias="largestMultiKill",
    )
    longest_time_spent_living: int = Field(
        alias="longestTimeSpentLiving",
    )
    magic_damage_dealt: int = Field(
        alias="magicDamageDealt",
    )
    magic_damage_dealt_to_champions: int = Field(
        alias="magicDamageDealtToChampions",
    )
    magic_damage_taken: int = Field(
        alias="magicDamageTaken",
    )
    missions: Optional[Missions] = Field(
        default=None,
        alias="missions",
    )
    need_vision_pings: Optional[int] = Field(
        default=None,
        alias="needVisionPings",
        description="Green ward",
    )
    neutral_minions_killed: int = Field(
        alias="neutralMinionsKilled",
        description="".join(
            (
                "neutralMinionsKilled = mNeutralMinionsKilled, ",
                "which is incremented on kills of kPet and kJun",
                "gleMonster",
            )
        ),
    )
    nexus_kills: int = Field(
        alias="nexusKills",
    )
    nexus_lost: Optional[int] = Field(
        default=None,
        alias="nexusLost",
    )
    nexus_takedowns: Optional[int] = Field(
        default=None,
        alias="nexusTakedowns",
    )
    objectives_stolen: int = Field(
        alias="objectivesStolen",
    )
    objectives_stolen_assists: int = Field(
        alias="objectivesStolenAssists",
    )
    on_my_way_pings: Optional[int] = Field(
        default=None,
        alias="onMyWayPings",
        description="Blue arrow pointing at ground",
    )
    participant_id: int = Field(
        alias="participantId",
    )
    penta_kills: int = Field(
        alias="pentaKills",
    )
    perks: Perks = Field(
        alias="perks",
    )
    physical_damage_dealt: int = Field(
        alias="physicalDamageDealt",
    )
    physical_damage_dealt_to_champions: int = Field(
        alias="physicalDamageDealtToChampions",
    )
    physical_damage_taken: int = Field(
        alias="physicalDamageTaken",
    )
    placement: Optional[int] = Field(
        default=None,
        alias="placement",
    )
    player_augment1: Optional[int] = Field(
        default=None,
        alias="playerAugment1",
    )
    player_augment2: Optional[int] = Field(
        default=None,
        alias="playerAugment2",
    )
    player_augment3: Optional[int] = Field(
        default=None,
        alias="playerAugment3",
    )
    player_augment4: Optional[int] = Field(
        default=None,
        alias="playerAugment4",
    )
    player_augment5: Optional[int] = Field(
        default=None,
        alias="playerAugment5",
    )
    player_augment6: Optional[int] = Field(
        default=None,
        alias="playerAugment6",
    )
    player_score0: Optional[float] = Field(
        default=None,
        alias="playerScore0",
    )
    player_score1: Optional[float] = Field(
        default=None,
        alias="playerScore1",
    )
    player_score10: Optional[float] = Field(
        default=None,
        alias="playerScore10",
    )
    player_score11: Optional[float] = Field(
        default=None,
        alias="playerScore11",
    )
    player_score2: Optional[float] = Field(
        default=None,
        alias="playerScore2",
    )
    player_score3: Optional[float] = Field(
        default=None,
        alias="playerScore3",
    )
    player_score4: Optional[float] = Field(
        default=None,
        alias="playerScore4",
    )
    player_score5: Optional[float] = Field(
        default=None,
        alias="playerScore5",
    )
    player_score6: Optional[float] = Field(
        default=None,
        alias="playerScore6",
    )
    player_score7: Optional[float] = Field(
        default=None,
        alias="playerScore7",
    )
    player_score8: Optional[float] = Field(
        default=None,
        alias="playerScore8",
    )
    player_score9: Optional[float] = Field(
        default=None,
        alias="playerScore9",
    )
    player_subteam_id: Optional[int] = Field(
        default=None,
        alias="playerSubteamId",
    )
    position_assigned_by_matchmaking: Optional[str] = Field(
        default=None,
        alias="positionAssignedByMatchmaking",
    )
    profile_icon: int = Field(
        alias="profileIcon",
    )
    push_pings: Optional[int] = Field(
        default=None,
        alias="pushPings",
        description="Green minion",
    )
    puuid: str = Field(
        alias="puuid",
    )
    quadra_kills: int = Field(
        alias="quadraKills",
    )
    retreat_pings: Optional[int] = Field(
        default=None,
        alias="retreatPings",
        description="".join(("https://github.com/RiotGames/developer-relatio", "ns/issues/814")),
    )
    riot_id_game_name: Optional[str] = Field(
        default=None,
        alias="riotIdGameName",
    )
    riot_id_name: Optional[str] = Field(
        default=None,
        alias="riotIdName",
        description="".join(
            (
                "Deprecated, use `riotIdGameName`. This field n",
                "ame was briefly used instead of `riotIdGameNam",
                "e`, prior to patch 14.5.",
            )
        ),
    )
    riot_id_tagline: Optional[str] = Field(
        default=None,
        alias="riotIdTagline",
    )
    role: str = Field(
        alias="role",
    )
    role_bound_item: Optional[int] = Field(
        default=None,
        alias="roleBoundItem",
    )
    selected_role_preferences: Optional[str] = Field(
        default=None,
        alias="selectedRolePreferences",
    )
    sight_wards_bought_in_game: int = Field(
        alias="sightWardsBoughtInGame",
    )
    spell1_casts: int = Field(
        alias="spell1Casts",
    )
    spell2_casts: int = Field(
        alias="spell2Casts",
    )
    spell3_casts: int = Field(
        alias="spell3Casts",
    )
    spell4_casts: int = Field(
        alias="spell4Casts",
    )
    subteam_placement: Optional[int] = Field(
        default=None,
        alias="subteamPlacement",
    )
    summoner1_casts: int = Field(
        alias="summoner1Casts",
    )
    summoner1_id: int = Field(
        alias="summoner1Id",
    )
    summoner2_casts: int = Field(
        alias="summoner2Casts",
    )
    summoner2_id: int = Field(
        alias="summoner2Id",
    )
    summoner_id: str = Field(
        alias="summonerId",
    )
    summoner_level: int = Field(
        alias="summonerLevel",
    )
    summoner_name: str = Field(
        alias="summonerName",
    )
    team_early_surrendered: bool = Field(
        alias="teamEarlySurrendered",
    )
    team_ignb_surrendered: Optional[bool] = Field(
        default=None,
        alias="teamIGNBSurrendered",
    )
    team_id: int = Field(
        alias="teamId",
    )
    team_position: str = Field(
        alias="teamPosition",
        description="".join(
            (
                "Both individualPosition and teamPosition are c",
                "omputed by the game server and are different v",
                "ersions of the most likely position played by ",
                "a player. The individualPosition is the best g",
                "uess for which position the player actually pl",
                "ayed in isolation of anything else. The teamPo",
                "sition is the best guess for which position th",
                "e player actually played if we add the constra",
                "int that each team must have one top player, o",
                "ne jungle, one middle, etc. Generally the reco",
                "mmendation is to use the teamPosition field ov",
                "er the individualPosition field.",
            )
        ),
    )
    time_c_cing_others: int = Field(
        alias="timeCCingOthers",
    )
    time_played: int = Field(
        alias="timePlayed",
    )
    total_ally_jungle_minions_killed: Optional[int] = Field(
        default=None,
        alias="totalAllyJungleMinionsKilled",
    )
    total_damage_dealt: int = Field(
        alias="totalDamageDealt",
    )
    total_damage_dealt_to_champions: int = Field(
        alias="totalDamageDealtToChampions",
    )
    total_damage_shielded_on_teammates: int = Field(
        alias="totalDamageShieldedOnTeammates",
    )
    total_damage_taken: int = Field(
        alias="totalDamageTaken",
    )
    total_enemy_jungle_minions_killed: Optional[int] = Field(
        default=None,
        alias="totalEnemyJungleMinionsKilled",
    )
    total_heal: int = Field(
        alias="totalHeal",
        description="".join(
            (
                "Whenever positive health is applied (which tra",
                "nslates to all heals in the game but not thing",
                "s like regeneration), totalHeal is incremented",
                " by the amount of health received. This includ",
                "es healing enemies, jungle monsters, yourself,",
                " etc",
            )
        ),
    )
    total_heals_on_teammates: int = Field(
        alias="totalHealsOnTeammates",
        description="".join(
            (
                "Whenever positive health is applied (which tra",
                "nslates to all heals in the game but not thing",
                "s like regeneration), totalHealsOnTeammates is",
                " incremented by the amount of health received.",
                "  This is post modified, so if you heal someon",
                "e missing 5 health for 100 you will get +5 tot",
                "alHealsOnTeammates",
            )
        ),
    )
    total_minions_killed: int = Field(
        alias="totalMinionsKilled",
        description="".join(
            (
                "totalMillionsKilled = mMinionsKilled, which is",
                " only incremented on kills of kTeamMinion, kMe",
                "leeLaneMinion, kSuperLaneMinion, kRangedLaneMi",
                "nion and kSiegeLaneMinion",
            )
        ),
    )
    total_time_cc_dealt: int = Field(
        alias="totalTimeCCDealt",
    )
    total_time_spent_dead: int = Field(
        alias="totalTimeSpentDead",
    )
    total_units_healed: int = Field(
        alias="totalUnitsHealed",
    )
    triple_kills: int = Field(
        alias="tripleKills",
    )
    true_damage_dealt: int = Field(
        alias="trueDamageDealt",
    )
    true_damage_dealt_to_champions: int = Field(
        alias="trueDamageDealtToChampions",
    )
    true_damage_taken: int = Field(
        alias="trueDamageTaken",
    )
    turret_kills: int = Field(
        alias="turretKills",
    )
    turret_takedowns: Optional[int] = Field(
        default=None,
        alias="turretTakedowns",
    )
    turrets_lost: Optional[int] = Field(
        default=None,
        alias="turretsLost",
    )
    unreal_kills: int = Field(
        alias="unrealKills",
    )
    vision_cleared_pings: Optional[int] = Field(
        default=None,
        alias="visionClearedPings",
    )
    vision_score: int = Field(
        alias="visionScore",
    )
    vision_wards_bought_in_game: int = Field(
        alias="visionWardsBoughtInGame",
    )
    wards_killed: int = Field(
        alias="wardsKilled",
    )
    wards_placed: int = Field(
        alias="wardsPlaced",
    )
    was_premade_with_ignb_game_end_causer: Optional[bool] = Field(
        default=None,
        alias="wasPremadeWithIGNBGameEndCauser",
    )
    was_premade_with_severe_transgressor: Optional[bool] = Field(
        default=None,
        alias="wasPremadeWithSevereTransgressor",
    )
    was_severe_transgressor: Optional[bool] = Field(
        default=None,
        alias="wasSevereTransgressor",
    )
    win: bool = Field(
        alias="win",
    )

    model_config = ConfigDict(populate_by_name=True)


class ParticipantFrame(BaseModel):
    champion_stats: ChampionStats = Field(
        alias="championStats",
    )
    current_gold: int = Field(
        alias="currentGold",
    )
    damage_stats: DamageStats = Field(
        alias="damageStats",
    )
    gold_per_second: int = Field(
        alias="goldPerSecond",
    )
    jungle_minions_killed: int = Field(
        alias="jungleMinionsKilled",
    )
    level: int = Field(
        alias="level",
    )
    minions_killed: int = Field(
        alias="minionsKilled",
    )
    participant_id: int = Field(
        alias="participantId",
    )
    position: Position = Field(
        alias="position",
    )
    time_enemy_spent_controlled: int = Field(
        alias="timeEnemySpentControlled",
    )
    total_gold: int = Field(
        alias="totalGold",
    )
    xp: int = Field(
        alias="xp",
    )

    model_config = ConfigDict(populate_by_name=True)


class ParticipantFrames(BaseModel):
    param_1_9: ParticipantFrame = Field(
        alias="1-9",
        description="Key value mapping for each participant",
    )

    model_config = ConfigDict(populate_by_name=True)


class ParticipantPlayerBehavior(BaseModel):
    player_behavior__is_hero_in_combat: Optional[int] = Field(
        default=None,
        alias="PlayerBehavior_IsHeroInCombat",
    )

    model_config = ConfigDict(populate_by_name=True)


class ParticipantTimeLine(BaseModel):
    participant_id: int = Field(
        alias="participantId",
    )
    puuid: str = Field(
        alias="puuid",
    )

    model_config = ConfigDict(populate_by_name=True)


class PerkStats(BaseModel):
    defense: int = Field(
        alias="defense",
    )
    flex: int = Field(
        alias="flex",
    )
    offense: int = Field(
        alias="offense",
    )

    model_config = ConfigDict(populate_by_name=True)


class PerkStyle(BaseModel):
    description: str = Field(
        alias="description",
    )
    selections: List[PerkStyleSelection] = Field(
        alias="selections",
    )
    style: int = Field(
        alias="style",
    )

    model_config = ConfigDict(populate_by_name=True)


class PerkStyleSelection(BaseModel):
    perk: int = Field(
        alias="perk",
    )
    var1: int = Field(
        alias="var1",
    )
    var2: int = Field(
        alias="var2",
    )
    var3: int = Field(
        alias="var3",
    )

    model_config = ConfigDict(populate_by_name=True)


class Perks(BaseModel):
    stat_perks: PerkStats = Field(
        alias="statPerks",
    )
    styles: List[PerkStyle] = Field(
        alias="styles",
    )

    model_config = ConfigDict(populate_by_name=True)


class Position(BaseModel):
    x: int = Field(
        alias="x",
    )
    y: int = Field(
        alias="y",
    )

    model_config = ConfigDict(populate_by_name=True)


class Replay(BaseModel):
    match_file_ur_ls: List[str] = Field(
        alias="matchFileURLs",
    )
    total: int = Field(
        alias="total",
        description="Total of replay files",
    )

    model_config = ConfigDict(populate_by_name=True)


class Team(BaseModel):
    bans: List[Ban] = Field(
        alias="bans",
    )
    feats: Optional[Feats] = Field(
        default=None,
        alias="feats",
    )
    objectives: Objectives = Field(
        alias="objectives",
    )
    team_id: int = Field(
        alias="teamId",
    )
    win: bool = Field(
        alias="win",
    )

    model_config = ConfigDict(populate_by_name=True)


class Timeline(BaseModel):
    info: InfoTimeLine = Field(
        alias="info",
        description="Match info.",
    )
    metadata: MetadataTimeLine = Field(
        alias="metadata",
        description="Match metadata.",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Ban,
    Challenges,
    ChampionStats,
    DamageStats,
    EventsTimeLine,
    Feat,
    Feats,
    FramesTimeLine,
    Info,
    InfoTimeLine,
    Match,
    MatchTimelineVictimDamage,
    Metadata,
    MetadataTimeLine,
    Missions,
    Objective,
    Objectives,
    Participant,
    ParticipantFrame,
    ParticipantFrames,
    ParticipantPlayerBehavior,
    ParticipantTimeLine,
    PerkStats,
    PerkStyle,
    PerkStyleSelection,
    Perks,
    Position,
    Replay,
    Team,
    Timeline,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type
