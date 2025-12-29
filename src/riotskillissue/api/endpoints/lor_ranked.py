# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Lor_rankedApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_leaderboards(
        self,
        region: str,
        
    ) -> lor_ranked_v1_LeaderboardDto:
        """
        Get the players in Master tier.
        """
        path = "/lor/ranked/v1/leaderboards"
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
        return TypeAdapter(lor_ranked_v1_LeaderboardDto).validate_python(response.json())
        
    