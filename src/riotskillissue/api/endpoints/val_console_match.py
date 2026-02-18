# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class ValConsoleMatchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match(
        self,
        region: Union[Region, Platform, str],
        
        matchId: str,
        
        
    ) -> val_console_match_v1_MatchDto:
        """Get match by id"""
        path = "/val/match/console/v1/matches/{matchId}"
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
        
        
        return TypeAdapter(val_console_match_v1_MatchDto).validate_python(response.json())
        
    
    async def get_matchlist(
        self,
        region: Union[Region, Platform, str],
        
        platformType: str,
        
        puuid: str,
        
        
    ) -> val_console_match_v1_MatchlistDto:
        """Get matchlist for games played by puuid and platform type"""
        path = "/val/match/console/v1/matchlists/by-puuid/{puuid}"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
            "platformType": platformType,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(val_console_match_v1_MatchlistDto).validate_python(response.json())
        
    
    async def get_recent(
        self,
        region: Union[Region, Platform, str],
        
        queue: str,
        
        
    ) -> val_console_match_v1_RecentMatchesDto:
        """Get recent matches"""
        path = "/val/match/console/v1/recent-matches/by-queue/{queue}"
        # Replace path params
        
        path = path.replace("{" + "queue" + "}", str(queue))
        

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
        
        
        return TypeAdapter(val_console_match_v1_RecentMatchesDto).validate_python(response.json())
        
    