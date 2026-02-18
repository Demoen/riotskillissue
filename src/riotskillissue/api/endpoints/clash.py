# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class ClashApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_players_by_puuid(
        self,
        region: Union[Region, Platform, str],
        
        puuid: str,
        
        
    ) -> List[clash_v1_PlayerDto]:
        """Get players by puuid"""
        path = "/lol/clash/v1/players/by-puuid/{puuid}"
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
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(List[clash_v1_PlayerDto]).validate_python(response.json())
        
    
    async def get_team_by_id(
        self,
        region: Union[Region, Platform, str],
        
        teamId: str,
        
        
    ) -> clash_v1_TeamDto:
        """Get team by ID."""
        path = "/lol/clash/v1/teams/{teamId}"
        # Replace path params
        
        path = path.replace("{" + "teamId" + "}", str(teamId))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(clash_v1_TeamDto).validate_python(response.json())
        
    
    async def get_tournaments(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> List[clash_v1_TournamentDto]:
        """Get all active or upcoming tournaments."""
        path = "/lol/clash/v1/tournaments"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(List[clash_v1_TournamentDto]).validate_python(response.json())
        
    
    async def get_tournament_by_team(
        self,
        region: Union[Region, Platform, str],
        
        teamId: str,
        
        
    ) -> clash_v1_TournamentDto:
        """Get tournament by team ID."""
        path = "/lol/clash/v1/tournaments/by-team/{teamId}"
        # Replace path params
        
        path = path.replace("{" + "teamId" + "}", str(teamId))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(clash_v1_TournamentDto).validate_python(response.json())
        
    
    async def get_tournament_by_id(
        self,
        region: Union[Region, Platform, str],
        
        tournamentId: int,
        
        
    ) -> clash_v1_TournamentDto:
        """Get tournament by ID."""
        path = "/lol/clash/v1/tournaments/{tournamentId}"
        # Replace path params
        
        path = path.replace("{" + "tournamentId" + "}", str(tournamentId))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(clash_v1_TournamentDto).validate_python(response.json())
        
    