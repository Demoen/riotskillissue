# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Lol-rso-matchApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_match_ids(
        self,
        region: str,
        
        count: int = None,
        
        start: int = None,
        
        type: str = None,
        
        queue: int = None,
        
        endTime: int = None,
        
        startTime: int = None,
        
    ) -> List[str]:
        """
        Get a list of match ids by player access token - Includes custom matches
        """
        path = "/lol/rso-match/v1/matches/ids"
        # Replace path params
        

        # Query params
        params = {
            
            "count": count,
            
            "start": start,
            
            "type": type,
            
            "queue": queue,
            
            "endTime": endTime,
            
            "startTime": startTime,
            
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
    
    async def get_match(
        self,
        region: str,
        
        matchId: str,
        
    ) -> match-v5.MatchDto:
        """
        Get a match by match id
        """
        path = "/lol/rso-match/v1/matches/{matchId}"
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
    
    async def get_timeline(
        self,
        region: str,
        
        matchId: str,
        
    ) -> match-v5.TimelineDto:
        """
        Get a match timeline by match id
        """
        path = "/lol/rso-match/v1/matches/{matchId}/timeline"
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
    