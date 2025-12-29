# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Tournament-stubApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def create_tournament_code(
        self,
        region: str,
        
        count: int = None,
        
        tournamentId: int,
        
    ) -> List[str]:
        """
        Create a tournament code for the given tournament - Stub method
        """
        path = "/lol/tournament-stub/v5/codes"
        # Replace path params
        

        # Query params
        params = {
            
            "count": count,
            
            "tournamentId": tournamentId,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region,
            params=params
        )
        return response.json()
    
    async def get_tournament_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> tournament-stub-v5.TournamentCodeV5DTO:
        """
        Returns the tournament code DTO associated with a tournament code string - Stub Method
        """
        path = "/lol/tournament-stub/v5/codes/{tournamentCode}"
        # Replace path params
        
        path = path.replace("{" + "tournamentCode" + "}", str(tournamentCode))
        

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
    
    async def get_lobby_events_by_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> tournament-stub-v5.LobbyEventV5DTOWrapper:
        """
        Gets a list of lobby events by tournament code - Stub method
        """
        path = "/lol/tournament-stub/v5/lobby-events/by-code/{tournamentCode}"
        # Replace path params
        
        path = path.replace("{" + "tournamentCode" + "}", str(tournamentCode))
        

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
    
    async def register_provider_data(
        self,
        region: str,
        
    ) -> int:
        """
        Creates a tournament provider and returns its ID - Stub method
        """
        path = "/lol/tournament-stub/v5/providers"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region,
            params=params
        )
        return response.json()
    
    async def register_tournament(
        self,
        region: str,
        
    ) -> int:
        """
        Creates a tournament and returns its ID - Stub method
        """
        path = "/lol/tournament-stub/v5/tournaments"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region,
            params=params
        )
        return response.json()
    