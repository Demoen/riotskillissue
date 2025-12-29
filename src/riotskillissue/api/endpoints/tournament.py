# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class TournamentApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def create_tournament_code(
        self,
        region: str,
        
        tournamentId: int,
        
        count: int = None,
        
    ) -> List[str]:
        """
        Create a tournament code for the given tournament.
        """
        path = "/lol/tournament/v5/codes"
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
        
    ) -> tournament_v5_TournamentCodeV5DTO:
        """
        Returns the tournament code DTO associated with a tournament code string.
        """
        path = "/lol/tournament/v5/codes/{tournamentCode}"
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
        return TypeAdapter(tournament_v5_TournamentCodeV5DTO).validate_python(response.json())
        
    
    async def update_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> None:
        """
        Update the pick type, map, spectator type, or allowed puuids for a code.
        """
        path = "/lol/tournament/v5/codes/{tournamentCode}"
        # Replace path params
        
        path = path.replace("{" + "tournamentCode" + "}", str(tournamentCode))
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        response = await self.http.request(
            method="PUT",
            url=path,
            region_or_platform=region,
            params=params
        )
        
        return response.json()
        
    
    async def get_games(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> List[tournament_v5_TournamentGamesV5]:
        """
        Get games details
        """
        path = "/lol/tournament/v5/games/by-code/{tournamentCode}"
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
        return TypeAdapter(List[tournament_v5_TournamentGamesV5]).validate_python(response.json())
        
    
    async def get_lobby_events_by_code(
        self,
        region: str,
        
        tournamentCode: str,
        
    ) -> tournament_v5_LobbyEventV5DTOWrapper:
        """
        Gets a list of lobby events by tournament code.
        """
        path = "/lol/tournament/v5/lobby-events/by-code/{tournamentCode}"
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
        return TypeAdapter(tournament_v5_LobbyEventV5DTOWrapper).validate_python(response.json())
        
    
    async def register_provider_data(
        self,
        region: str,
        
    ) -> int:
        """
        Creates a tournament provider and returns its ID.
        """
        path = "/lol/tournament/v5/providers"
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
        Creates a tournament and returns its ID.
        """
        path = "/lol/tournament/v5/tournaments"
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
        
    