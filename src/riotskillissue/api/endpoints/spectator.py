# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class SpectatorApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_current_game_info_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> spectator_v5_CurrentGameInfo:
        """
        Get current game information for the given puuid.
        """
        path = "/lol/spectator/v5/active-games/by-summoner/{encryptedPUUID}"
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
        return TypeAdapter(spectator_v5_CurrentGameInfo).validate_python(response.json())
        
    