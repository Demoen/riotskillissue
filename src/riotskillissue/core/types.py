from typing import NewType, Dict

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum
    class StrEnum(str, Enum):
        pass

class Region(StrEnum):

    BR1 = "br1"
    EUN1 = "eun1"
    EUW1 = "euw1"
    JP1 = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    NA1 = "na1"
    OC1 = "oc1"
    TR1 = "tr1"
    RU = "ru"
    PH2 = "ph2"
    SG2 = "sg2"
    TH2 = "th2"
    TW2 = "tw2"
    VN2 = "vn2"

class Platform(StrEnum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    SEA = "sea"

# Helper to map Region -> Platform
REGION_TO_PLATFORM: Dict[Region, Platform] = {
    Region.BR1: Platform.AMERICAS,
    Region.NA1: Platform.AMERICAS,
    Region.LA1: Platform.AMERICAS,
    Region.LA2: Platform.AMERICAS,
    Region.KR: Platform.ASIA,
    Region.JP1: Platform.ASIA,
    Region.EUN1: Platform.EUROPE,
    Region.EUW1: Platform.EUROPE,
    Region.TR1: Platform.EUROPE,
    Region.RU: Platform.EUROPE,
    Region.OC1: Platform.SEA,
    Region.PH2: Platform.SEA,
    Region.SG2: Platform.SEA,
    Region.TH2: Platform.SEA,
    Region.TW2: Platform.SEA,
    Region.VN2: Platform.SEA,
}

Puuid = NewType("Puuid", str)
SummonerId = NewType("SummonerId", str)
AccountId = NewType("AccountId", str)
