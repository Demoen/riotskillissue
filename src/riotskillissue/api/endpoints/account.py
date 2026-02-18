# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class AccountApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        puuid: str,
        
        
    ) -> account_v1_AccountDto:
        """Get account by puuid"""
        path = "/riot/account/v1/accounts/by-puuid/{puuid}"
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
        
        
        return TypeAdapter(account_v1_AccountDto).validate_python(response.json())
        
    
    async def get_by_riot_id(
        self,
        region: Union[Region, Platform, str],
        
        gameName: str,
        
        tagLine: str,
        
        
    ) -> account_v1_AccountDto:
        """Get account by riot id"""
        path = "/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        # Replace path params
        
        path = path.replace("{" + "gameName" + "}", str(gameName))
        
        path = path.replace("{" + "tagLine" + "}", str(tagLine))
        

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
        
        
        return TypeAdapter(account_v1_AccountDto).validate_python(response.json())
        
    
    async def get_by_access_token(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> account_v1_AccountDto:
        """Get account by access token"""
        path = "/riot/account/v1/accounts/me"
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
        
        
        return TypeAdapter(account_v1_AccountDto).validate_python(response.json())
        
    
    async def get_active_shard(
        self,
        region: Union[Region, Platform, str],
        
        game: str,
        
        puuid: str,
        
        
    ) -> account_v1_ActiveShardDto:
        """Get active shard for a player"""
        path = "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}"
        # Replace path params
        
        path = path.replace("{" + "game" + "}", str(game))
        
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
        
        
        return TypeAdapter(account_v1_ActiveShardDto).validate_python(response.json())
        
    
    async def get_active_region(
        self,
        region: Union[Region, Platform, str],
        
        game: str,
        
        puuid: str,
        
        
    ) -> account_v1_AccountRegionDTO:
        """Get active region (lol and tft)"""
        path = "/riot/account/v1/region/by-game/{game}/by-puuid/{puuid}"
        # Replace path params
        
        path = path.replace("{" + "game" + "}", str(game))
        
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
        
        
        return TypeAdapter(account_v1_AccountRegionDTO).validate_python(response.json())
        
    