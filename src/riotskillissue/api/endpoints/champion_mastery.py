# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Champion_masteryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_all_champion_masteries_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> List[champion_mastery_v4_ChampionMasteryDto]:
        """
        Get all champion mastery entries sorted by number of champion points descending.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[champion_mastery_v4_ChampionMasteryDto]).validate_python(response.json())
        
    
    async def get_champion_mastery_by_puuid(
        self,
        region: str,
        
        championId: int,
        
        encryptedPUUID: str,
        
    ) -> champion_mastery_v4_ChampionMasteryDto:
        """
        Get a champion mastery by puuid and champion ID.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(champion_mastery_v4_ChampionMasteryDto).validate_python(response.json())
        
    
    async def get_top_champion_masteries_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
        count: int = None,
        
    ) -> List[champion_mastery_v4_ChampionMasteryDto]:
        """
        Get specified number of top champion mastery entries sorted by number of champion points descending.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[champion_mastery_v4_ChampionMasteryDto]).validate_python(response.json())
        
    
    async def get_champion_mastery_score_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> int:
        """
        Get a player's total champion mastery score, which is the sum of individual champion mastery levels.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(int).validate_python(response.json())
        
    