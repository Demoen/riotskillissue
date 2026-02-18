# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class MatchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match_ids_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        puuid: str,
        
        count: int = None,
        
        endTime: int = None,
        
        queue: int = None,
        
        start: int = None,
        
        startTime: int = None,
        
        type: str = None,
        
        
    ) -> List[str]:
        """Get a list of match ids by puuid"""
        path = "/lol/match/v5/matches/by-puuid/{puuid}/ids"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
            "count": count,
            
            "endTime": endTime,
            
            "queue": queue,
            
            "start": start,
            
            "startTime": startTime,
            
            "type": type,
            
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
        
    
    async def get_replay(
        self,
        region: Union[Region, Platform, str],
        
        puuid: str,
        
        
    ) -> match_v5_ReplayDTO:
        """Get player replays"""
        path = "/lol/match/v5/matches/by-puuid/{puuid}/replays"
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
        
        
        return TypeAdapter(match_v5_ReplayDTO).validate_python(response.json())
        
    
    async def get_match(
        self,
        region: Union[Region, Platform, str],
        
        matchId: str,
        
        
    ) -> match_v5_MatchDto:
        """Get a match by match id"""
        path = "/lol/match/v5/matches/{matchId}"
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
        
        
        return TypeAdapter(match_v5_MatchDto).validate_python(response.json())
        
    
    async def get_timeline(
        self,
        region: Union[Region, Platform, str],
        
        matchId: str,
        
        
    ) -> match_v5_TimelineDto:
        """Get a match timeline by match id"""
        path = "/lol/match/v5/matches/{matchId}/timeline"
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
        
        
        return TypeAdapter(match_v5_TimelineDto).validate_python(response.json())
        
    