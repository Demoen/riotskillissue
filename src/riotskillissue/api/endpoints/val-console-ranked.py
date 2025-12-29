# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Val-console-rankedApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_leaderboard(
        self,
        region: str,
        
        actId: str,
        
        platformType: str,
        
        startIndex: int = None,
        
        size: int = None,
        
    ) -> val-console-ranked-v1.LeaderboardDto:
        """
        Get leaderboard for the competitive queue
        """
        path = "/val/console/ranked/v1/leaderboards/by-act/{actId}"
        # Replace path params
        
        path = path.replace("{" + "actId" + "}", str(actId))
        

        # Query params
        params = {
            
            "platformType": platformType,
            
            "startIndex": startIndex,
            
            "size": size,
            
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
    