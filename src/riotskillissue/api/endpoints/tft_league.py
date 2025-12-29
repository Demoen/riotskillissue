# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Tft_leagueApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_league_entries_by_puuid(
        self,
        region: str,
        
        puuid: str,
        
    ) -> List[tft_league_v1_LeagueEntryDTO]:
        """
        Get league entries in all queues for a given puuid
        """
        path = "/tft/league/v1/by-puuid/{puuid}"
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
        return TypeAdapter(List[tft_league_v1_LeagueEntryDTO]).validate_python(response.json())
        
    
    async def get_challenger_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft_league_v1_LeagueListDTO:
        """
        Get the challenger league.
        """
        path = "/tft/league/v1/challenger"
        # Replace path params
        

        # Query params
        params = {
            
            "queue": queue,
            
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
        return TypeAdapter(tft_league_v1_LeagueListDTO).validate_python(response.json())
        
    
    async def get_league_entries(
        self,
        region: str,
        
        division: str,
        
        tier: str,
        
        page: int = None,
        
        queue: str = None,
        
    ) -> List[tft_league_v1_LeagueEntryDTO]:
        """
        Get all the league entries.
        """
        path = "/tft/league/v1/entries/{tier}/{division}"
        # Replace path params
        
        path = path.replace("{" + "division" + "}", str(division))
        
        path = path.replace("{" + "tier" + "}", str(tier))
        

        # Query params
        params = {
            
            "page": page,
            
            "queue": queue,
            
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
        return TypeAdapter(List[tft_league_v1_LeagueEntryDTO]).validate_python(response.json())
        
    
    async def get_grandmaster_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft_league_v1_LeagueListDTO:
        """
        Get the grandmaster league.
        """
        path = "/tft/league/v1/grandmaster"
        # Replace path params
        

        # Query params
        params = {
            
            "queue": queue,
            
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
        return TypeAdapter(tft_league_v1_LeagueListDTO).validate_python(response.json())
        
    
    async def get_league_by_id(
        self,
        region: str,
        
        leagueId: str,
        
    ) -> tft_league_v1_LeagueListDTO:
        """
        Get league with given ID, including inactive entries.
        """
        path = "/tft/league/v1/leagues/{leagueId}"
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
        return TypeAdapter(tft_league_v1_LeagueListDTO).validate_python(response.json())
        
    
    async def get_master_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft_league_v1_LeagueListDTO:
        """
        Get the master league.
        """
        path = "/tft/league/v1/master"
        # Replace path params
        

        # Query params
        params = {
            
            "queue": queue,
            
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
        return TypeAdapter(tft_league_v1_LeagueListDTO).validate_python(response.json())
        
    
    async def get_top_rated_ladder(
        self,
        region: str,
        
        queue: str,
        
    ) -> List[tft_league_v1_TopRatedLadderEntryDto]:
        """
        Get the top rated ladder for given queue
        """
        path = "/tft/league/v1/rated-ladders/{queue}/top"
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
        return TypeAdapter(List[tft_league_v1_TopRatedLadderEntryDto]).validate_python(response.json())
        
    