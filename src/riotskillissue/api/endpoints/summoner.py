# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class SummonerApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        encryptedPUUID: str,
        
        
    ) -> summoner_v4_SummonerDTO:
        """Get a summoner by PUUID."""
        path = "/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
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
        
        
        return TypeAdapter(summoner_v4_SummonerDTO).validate_python(response.json())
        
    
    async def get_by_access_token(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> summoner_v4_SummonerDTO:
        """Get a summoner by access token."""
        path = "/lol/summoner/v4/summoners/me"
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
        
        
        return TypeAdapter(summoner_v4_SummonerDTO).validate_python(response.json())
        
    