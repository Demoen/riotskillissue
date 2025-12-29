# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Tft-matchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match_ids_by_p_u_u_i_d(
        self,
        region: str,
        
        puuid: str,
        
        start: int = None,
        
        endTime: int = None,
        
        startTime: int = None,
        
        count: int = None,
        
    ) -> List[str]:
        """
        Get a list of match ids by PUUID
        """
        path = "/tft/match/v1/matches/by-puuid/{puuid}/ids"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
            "start": start,
            
            "endTime": endTime,
            
            "startTime": startTime,
            
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
    
    async def get_match(
        self,
        region: str,
        
        matchId: str,
        
    ) -> tft-match-v1.MatchDto:
        """
        Get a match by match id
        """
        path = "/tft/match/v1/matches/{matchId}"
        # Replace path params
        
        path = path.replace("{" + "matchId" + "}", str(matchId))
        

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
    