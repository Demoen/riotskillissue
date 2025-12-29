# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Val_console_rankedApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_leaderboard(
        self,
        region: str,
        
        actId: str,
        
        platformType: str,
        
        size: int = None,
        
        startIndex: int = None,
        
    ) -> val_console_ranked_v1_LeaderboardDto:
        """
        Get leaderboard for the competitive queue
        """
        path = "/val/console/ranked/v1/leaderboards/by-act/{actId}"
        # Replace path params
        
        path = path.replace("{" + "actId" + "}", str(actId))
        

        # Query params
        params = {
            
            "platformType": platformType,
            
            "size": size,
            
            "startIndex": startIndex,
            
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
        return TypeAdapter(val_console_ranked_v1_LeaderboardDto).validate_python(response.json())
        
    