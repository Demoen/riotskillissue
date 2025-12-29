# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Spectator-tftApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_current_game_info_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> spectator-tft-v5.CurrentGameInfo:
        """
        Get current game information for the given puuid.
        """
        path = "/lol/spectator/tft/v5/active-games/by-puuid/{encryptedPUUID}"
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
        return response.json()
    