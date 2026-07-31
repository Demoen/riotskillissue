from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Act(BaseModel):
    id: str = Field(
        alias="id",
    )
    is_active: bool = Field(
        alias="isActive",
    )
    localized_names: Optional[LocalizedNames] = Field(
        default=None,
        alias="localizedNames",
        description="".join(("This field is excluded from the response when ", "a locale is set")),
    )
    name: str = Field(
        alias="name",
    )
    parent_id: Optional[str] = Field(
        default=None,
        alias="parentId",
    )
    type: Optional[str] = Field(
        default=None,
        alias="type",
    )

    model_config = ConfigDict(populate_by_name=True)


class Content(BaseModel):
    acts: List[Act] = Field(
        alias="acts",
    )
    ceremonies: Optional[List[ContentItem]] = Field(
        default=None,
        alias="ceremonies",
    )
    characters: List[ContentItem] = Field(
        alias="characters",
    )
    charm_levels: List[ContentItem] = Field(
        alias="charmLevels",
    )
    charms: List[ContentItem] = Field(
        alias="charms",
    )
    chromas: List[ContentItem] = Field(
        alias="chromas",
    )
    equips: List[ContentItem] = Field(
        alias="equips",
    )
    game_modes: List[ContentItem] = Field(
        alias="gameModes",
    )
    maps: List[ContentItem] = Field(
        alias="maps",
    )
    player_cards: List[ContentItem] = Field(
        alias="playerCards",
    )
    player_titles: List[ContentItem] = Field(
        alias="playerTitles",
    )
    skin_levels: List[ContentItem] = Field(
        alias="skinLevels",
    )
    skins: List[ContentItem] = Field(
        alias="skins",
    )
    spray_levels: List[ContentItem] = Field(
        alias="sprayLevels",
    )
    sprays: List[ContentItem] = Field(
        alias="sprays",
    )
    totems: Optional[List[ContentItem]] = Field(
        default=None,
        alias="totems",
    )
    version: str = Field(
        alias="version",
    )

    model_config = ConfigDict(populate_by_name=True)


class ContentItem(BaseModel):
    asset_name: str = Field(
        alias="assetName",
    )
    asset_path: Optional[str] = Field(
        default=None,
        alias="assetPath",
        description="".join(
            (
                "This field is only included for maps and game ",
                "modes. These values are used in the match resp",
                "onse.",
            )
        ),
    )
    id: str = Field(
        alias="id",
    )
    localized_names: Optional[LocalizedNames] = Field(
        default=None,
        alias="localizedNames",
        description="".join(("This field is excluded from the response when ", "a locale is set")),
    )
    name: str = Field(
        alias="name",
    )

    model_config = ConfigDict(populate_by_name=True)


class LocalizedNames(BaseModel):
    ar_ae: str = Field(
        alias="ar-AE",
    )
    de_de: str = Field(
        alias="de-DE",
    )
    en_gb: Optional[str] = Field(
        default=None,
        alias="en-GB",
    )
    en_us: str = Field(
        alias="en-US",
    )
    es_es: str = Field(
        alias="es-ES",
    )
    es_mx: str = Field(
        alias="es-MX",
    )
    fr_fr: str = Field(
        alias="fr-FR",
    )
    id_id: str = Field(
        alias="id-ID",
    )
    it_it: str = Field(
        alias="it-IT",
    )
    ja_jp: str = Field(
        alias="ja-JP",
    )
    ko_kr: str = Field(
        alias="ko-KR",
    )
    pl_pl: str = Field(
        alias="pl-PL",
    )
    pt_br: str = Field(
        alias="pt-BR",
    )
    ru_ru: str = Field(
        alias="ru-RU",
    )
    th_th: str = Field(
        alias="th-TH",
    )
    tr_tr: str = Field(
        alias="tr-TR",
    )
    vi_vn: str = Field(
        alias="vi-VN",
    )
    zh_cn: str = Field(
        alias="zh-CN",
    )
    zh_tw: str = Field(
        alias="zh-TW",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Act,
    Content,
    ContentItem,
    LocalizedNames,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type
