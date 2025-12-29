# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Tft_matchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match_ids_by_puuid(
        self,
        region: str,
        
        puuid: str,
        
        count: int = None,
        
        endTime: int = None,
        
        start: int = None,
        
        startTime: int = None,
        
    ) -> List[str]:
        """
        Get a list of match ids by PUUID
        """
        path = "/tft/match/v1/matches/by-puuid/{puuid}/ids"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
            "count": count,
            
            "endTime": endTime,
            
            "start": start,
            
            "startTime": startTime,
            
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
        return TypeAdapter(List[str]).validate_python(response.json())
        
    
    async def get_match(
        self,
        region: str,
        
        matchId: str,
        
    ) -> tft_match_v1_MatchDto:
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(tft_match_v1_MatchDto).validate_python(response.json())
        
    