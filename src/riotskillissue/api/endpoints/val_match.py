# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Val_matchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match(
        self,
        region: str,
        
        matchId: str,
        
    ) -> val_match_v1_MatchDto:
        """
        Get match by id
        """
        path = "/val/match/v1/matches/{matchId}"
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(val_match_v1_MatchDto).validate_python(response.json())
        
    
    async def get_matchlist(
        self,
        region: str,
        
        puuid: str,
        
    ) -> val_match_v1_MatchlistDto:
        """
        Get matchlist for games played by puuid
        """
        path = "/val/match/v1/matchlists/by-puuid/{puuid}"
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(val_match_v1_MatchlistDto).validate_python(response.json())
        
    
    async def get_recent(
        self,
        region: str,
        
        queue: str,
        
    ) -> val_match_v1_RecentMatchesDto:
        """
        Get recent matches
        """
        path = "/val/match/v1/recent-matches/by-queue/{queue}"
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(val_match_v1_RecentMatchesDto).validate_python(response.json())
        
    