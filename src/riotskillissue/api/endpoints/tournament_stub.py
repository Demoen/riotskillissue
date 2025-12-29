# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Tournament_stubApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def create_tournament_code(
        self,
        region: str,
        
        tournamentId: int,
        
        count: int = None,
        
    ) -> List[str]:
        """
        Create a tournament code for the given tournament - Stub method
        """
        path = "/lol/tournament-stub/v5/codes"
        # Replace path params
        

        # Query params
        params = {
            
            "tournamentId": tournamentId,
            
            "count": count,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[str]).validate_python(response.json())
        
    
    async def get_tournament_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> tournament_stub_v5_TournamentCodeV5DTO:
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(tournament_stub_v5_TournamentCodeV5DTO).validate_python(response.json())
        
    
    async def get_lobby_events_by_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> tournament_stub_v5_LobbyEventV5DTOWrapper:
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(tournament_stub_v5_LobbyEventV5DTOWrapper).validate_python(response.json())
        
    
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(int).validate_python(response.json())
        
    
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(int).validate_python(response.json())
        
    