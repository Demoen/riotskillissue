# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class League-expApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_league_entries(
        self,
        region: str,
        
        queue: str,
        
        tier: str,
        
        division: str,
        
        page: int = None,
        
    ) -> List[league-exp-v4.LeagueEntryDTO]:
        """
        Get all the league entries.
        """
        path = "/lol/league-exp/v4/entries/{queue}/{tier}/{division}"
        # Replace path params
        
        path = path.replace("{" + "queue" + "}", str(queue))
        
        path = path.replace("{" + "tier" + "}", str(tier))
        
        path = path.replace("{" + "division" + "}", str(division))
        

        # Query params
        params = {
            
            "page": page,
            
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
    