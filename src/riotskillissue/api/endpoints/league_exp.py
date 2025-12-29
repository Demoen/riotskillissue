# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class League_expApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_league_entries(
        self,
        region: str,
        
        division: str,
        
        queue: str,
        
        tier: str,
        
        page: int = None,
        
    ) -> List[league_exp_v4_LeagueEntryDTO]:
        """
        Get all the league entries.
        """
        path = "/lol/league-exp/v4/entries/{queue}/{tier}/{division}"
        # Replace path params
        
        path = path.replace("{" + "division" + "}", str(division))
        
        path = path.replace("{" + "queue" + "}", str(queue))
        
        path = path.replace("{" + "tier" + "}", str(tier))
        

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
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[league_exp_v4_LeagueEntryDTO]).validate_python(response.json())
        
    