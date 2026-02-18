# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class LorMatchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match_ids_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        puuid: str,
        
        
    ) -> List[str]:
        """Get a list of match ids by PUUID"""
        path = "/lor/match/v1/matches/by-puuid/{puuid}/ids"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

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
        
        
        return TypeAdapter(List[str]).validate_python(response.json())
        
    
    async def get_match(
        self,
        region: Union[Region, Platform, str],
        
        matchId: str,
        
        
    ) -> lor_match_v1_MatchDto:
        """Get match by id"""
        path = "/lor/match/v1/matches/{matchId}"
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
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(lor_match_v1_MatchDto).validate_python(response.json())
        
    