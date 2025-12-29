# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Val-console-matchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match(
        self,
        region: str,
        
        matchId: str,
        
    ) -> val-console-match-v1.MatchDto:
        """
        Get match by id
        """
        path = "/val/match/console/v1/matches/{matchId}"
        # Replace path params
        
        path = path.replace("{" + "matchId" + "}", str(matchId))
        

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
    
    async def get_matchlist(
        self,
        region: str,
        
        puuid: str,
        
        platformType: str,
        
    ) -> val-console-match-v1.MatchlistDto:
        """
        Get matchlist for games played by puuid and platform type
        """
        path = "/val/match/console/v1/matchlists/by-puuid/{puuid}"
        # Replace path params
        
        path = path.replace("{" + "puuid" + "}", str(puuid))
        

        # Query params
        params = {
            
            "platformType": platformType,
            
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
    
    async def get_recent(
        self,
        region: str,
        
        queue: str,
        
    ) -> val-console-match-v1.RecentMatchesDto:
        """
        Get recent matches
        """
        path = "/val/match/console/v1/recent-matches/by-queue/{queue}"
        # Replace path params
        
        path = path.replace("{" + "queue" + "}", str(queue))
        

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
    