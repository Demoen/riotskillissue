# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class ChampionMasteryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_all_champion_masteries_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        encryptedPUUID: str,
        
        
    ) -> List[champion_mastery_v4_ChampionMasteryDto]:
        """Get all champion mastery entries sorted by number of champion points descending."""
        path = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}"
        # Replace path params
        
        path = path.replace("{" + "encryptedPUUID" + "}", str(encryptedPUUID))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(List[champion_mastery_v4_ChampionMasteryDto]).validate_python(response.json())
        
    
    async def get_champion_mastery_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        championId: int,
        
        encryptedPUUID: str,
        
        
    ) -> champion_mastery_v4_ChampionMasteryDto:
        """Get a champion mastery by puuid and champion ID."""
        path = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/by-champion/{championId}"
        # Replace path params
        
        path = path.replace("{" + "championId" + "}", str(championId))
        
        path = path.replace("{" + "encryptedPUUID" + "}", str(encryptedPUUID))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(champion_mastery_v4_ChampionMasteryDto).validate_python(response.json())
        
    
    async def get_top_champion_masteries_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        encryptedPUUID: str,
        
        count: Optional[int] = None,
        
        
    ) -> List[champion_mastery_v4_ChampionMasteryDto]:
        """Get specified number of top champion mastery entries sorted by number of champion points descending."""
        path = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top"
        # Replace path params
        
        path = path.replace("{" + "encryptedPUUID" + "}", str(encryptedPUUID))
        

        # Query params
        params = {
            
            "count": count,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(List[champion_mastery_v4_ChampionMasteryDto]).validate_python(response.json())
        
    
    async def get_champion_mastery_score_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        encryptedPUUID: str,
        
        
    ) -> int:
        """Get a player's total champion mastery score, which is the sum of individual champion mastery levels."""
        path = "/lol/champion-mastery/v4/scores/by-puuid/{encryptedPUUID}"
        # Replace path params
        
        path = path.replace("{" + "encryptedPUUID" + "}", str(encryptedPUUID))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(int).validate_python(response.json())
        
    