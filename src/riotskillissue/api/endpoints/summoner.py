# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class SummonerApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> summoner_v4_SummonerDTO:
        """
        Get a summoner by PUUID.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(summoner_v4_SummonerDTO).validate_python(response.json())
        
    
    async def get_by_access_token(
        self,
        region: str,
        
    ) -> summoner_v4_SummonerDTO:
        """
        Get a summoner by access token.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(summoner_v4_SummonerDTO).validate_python(response.json())
        
    