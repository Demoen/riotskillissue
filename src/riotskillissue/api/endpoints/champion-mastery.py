# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Champion-masteryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_all_champion_masteries_by_p_u_u_i_d(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> List[champion-mastery-v4.ChampionMasteryDto]:
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
        return response.json()
    
    async def get_champion_mastery_by_p_u_u_i_d(
        self,
        region: str,
        
        encryptedPUUID: str,
        
        championId: int,
        
    ) -> champion-mastery-v4.ChampionMasteryDto:
        """
        Get a champion mastery by puuid and champion ID.
        """
        path = "/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/by-champion/{championId}"
        # Replace path params
        
        path = path.replace("{" + "encryptedPUUID" + "}", str(encryptedPUUID))
        
        path = path.replace("{" + "championId" + "}", str(championId))
        

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
        return response.json()
    
    async def get_top_champion_masteries_by_p_u_u_i_d(
        self,
        region: str,
        
        encryptedPUUID: str,
        
        count: int = None,
        
    ) -> List[champion-mastery-v4.ChampionMasteryDto]:
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
        return response.json()
    
    async def get_champion_mastery_score_by_p_u_u_i_d(
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
        return response.json()
    