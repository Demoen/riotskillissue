# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class LeagueApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_challenger_league(
        self,
        region: str,
        
        queue: str,
        
    ) -> league_v4_LeagueListDTO:
        """
        Get the challenger league for given queue.
        """
        path = "/lol/league/v4/challengerleagues/by-queue/{queue}"
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
        return TypeAdapter(league_v4_LeagueListDTO).validate_python(response.json())
        
    
    async def get_league_entries_by_puuid(
        self,
        region: str,
        
        encryptedPUUID: str,
        
    ) -> List[league_v4_LeagueEntryDTO]:
        """
        Get league entries in all queues for a given puuid
        """
        path = "/lol/league/v4/entries/by-puuid/{encryptedPUUID}"
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
        return TypeAdapter(List[league_v4_LeagueEntryDTO]).validate_python(response.json())
        
    
    async def get_league_entries(
        self,
        region: str,
        
        division: str,
        
        queue: str,
        
        tier: str,
        
        page: int = None,
        
    ) -> List[league_v4_LeagueEntryDTO]:
        """
        Get all the league entries.
        """
        path = "/lol/league/v4/entries/{queue}/{tier}/{division}"
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
        return TypeAdapter(List[league_v4_LeagueEntryDTO]).validate_python(response.json())
        
    
    async def get_grandmaster_league(
        self,
        region: str,
        
        queue: str,
        
    ) -> league_v4_LeagueListDTO:
        """
        Get the grandmaster league of a specific queue.
        """
        path = "/lol/league/v4/grandmasterleagues/by-queue/{queue}"
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
        return TypeAdapter(league_v4_LeagueListDTO).validate_python(response.json())
        
    
    async def get_league_by_id(
        self,
        region: str,
        
        leagueId: str,
        
    ) -> league_v4_LeagueListDTO:
        """
        Get league with given ID, including inactive entries.
        """
        path = "/lol/league/v4/leagues/{leagueId}"
        # Replace path params
        
        path = path.replace("{" + "leagueId" + "}", str(leagueId))
        

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
        return TypeAdapter(league_v4_LeagueListDTO).validate_python(response.json())
        
    
    async def get_master_league(
        self,
        region: str,
        
        queue: str,
        
    ) -> league_v4_LeagueListDTO:
        """
        Get the master league for given queue.
        """
        path = "/lol/league/v4/masterleagues/by-queue/{queue}"
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
        return TypeAdapter(league_v4_LeagueListDTO).validate_python(response.json())
        
    