# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class ChampionApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_champion_info(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> champion_v3_ChampionInfo:
        """Returns champion rotations, including free-to-play and low-level free-to-play rotations (REST)"""
        path = "/lol/platform/v3/champion-rotations"
        # Replace path params
        

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
        
        
        return TypeAdapter(champion_v3_ChampionInfo).validate_python(response.json())
        
    