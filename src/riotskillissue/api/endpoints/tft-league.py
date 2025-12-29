# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Tft-leagueApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_league_entries_by_p_u_u_i_d(
        self,
        region: str,
        
        puuid: str,
        
    ) -> List[tft-league-v1.LeagueEntryDTO]:
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
        return response.json()
    
    async def get_challenger_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft-league-v1.LeagueListDTO:
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
        return response.json()
    
    async def get_league_entries(
        self,
        region: str,
        
        tier: str,
        
        division: str,
        
        queue: str = None,
        
        page: int = None,
        
    ) -> List[tft-league-v1.LeagueEntryDTO]:
        """
        Get all the league entries.
        """
        path = "/tft/league/v1/entries/{tier}/{division}"
        # Replace path params
        
        path = path.replace("{" + "tier" + "}", str(tier))
        
        path = path.replace("{" + "division" + "}", str(division))
        

        # Query params
        params = {
            
            "queue": queue,
            
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
    
    async def get_grandmaster_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft-league-v1.LeagueListDTO:
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
        return response.json()
    
    async def get_league_by_id(
        self,
        region: str,
        
        leagueId: str,
        
    ) -> tft-league-v1.LeagueListDTO:
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
        return response.json()
    
    async def get_master_league(
        self,
        region: str,
        
        queue: str = None,
        
    ) -> tft-league-v1.LeagueListDTO:
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
        return response.json()
    
    async def get_top_rated_ladder(
        self,
        region: str,
        
        queue: str,
        
    ) -> List[tft-league-v1.TopRatedLadderEntryDto]:
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
        return response.json()
    