# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class ValRankedApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_leaderboard(
        self,
        region: Union[Region, Platform, str],
        
        actId: str,
        
        size: int = None,
        
        startIndex: int = None,
        
        
    ) -> val_ranked_v1_LeaderboardDto:
        """Get leaderboard for the competitive queue"""
        path = "/val/ranked/v1/leaderboards/by-act/{actId}"
        # Replace path params
        
        path = path.replace("{" + "actId" + "}", str(actId))
        

        # Query params
        params = {
            
            "size": size,
            
            "startIndex": startIndex,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(val_ranked_v1_LeaderboardDto).validate_python(response.json())
        
    