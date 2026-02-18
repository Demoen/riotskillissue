# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class TftSummonerApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        encryptedPUUID: str,
        
        
    ) -> tft_summoner_v1_SummonerDTO:
        """Get a summoner by PUUID."""
        path = "/tft/summoner/v1/summoners/by-puuid/{encryptedPUUID}"
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
        
        
        return TypeAdapter(tft_summoner_v1_SummonerDTO).validate_python(response.json())
        
    
    async def get_by_access_token(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> tft_summoner_v1_SummonerDTO:
        """Get a summoner by access token."""
        path = "/tft/summoner/v1/summoners/me"
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
        
        
        return TypeAdapter(tft_summoner_v1_SummonerDTO).validate_python(response.json())
        
    