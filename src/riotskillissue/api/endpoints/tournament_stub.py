# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class TournamentStubApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def create_tournament_code(
        self,
        region: Union[Region, Platform, str],
        
        tournamentId: int,
        
        count: Optional[int] = None,
        
        
        body: Optional[tournament_stub_v5_TournamentCodeParametersV5] = None,
        
    ) -> List[str]:
        """Create a tournament code for the given tournament - Stub method"""
        path = "/lol/tournament-stub/v5/codes"
        # Replace path params
        

        # Query params
        params = {
            
            "tournamentId": tournamentId,
            
            "count": count,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        kwargs: Dict[str, Any] = {"params": params}
        if body is not None:
            if hasattr(body, "model_dump"):
                kwargs["json"] = body.model_dump(by_alias=True, exclude_none=True)
            else:
                kwargs["json"] = body
        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            **kwargs
        )
        
        
        return TypeAdapter(List[str]).validate_python(response.json())
        
    
    async def get_tournament_code(
        self,
        region: Union[Region, Platform, str],
        
        tournamentCode: str,
        
        
    ) -> tournament_stub_v5_TournamentCodeV5DTO:
        """Returns the tournament code DTO associated with a tournament code string - Stub Method"""
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
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(tournament_stub_v5_TournamentCodeV5DTO).validate_python(response.json())
        
    
    async def get_lobby_events_by_code(
        self,
        region: Union[Region, Platform, str],
        
        tournamentCode: str,
        
        
    ) -> tournament_stub_v5_LobbyEventV5DTOWrapper:
        """Gets a list of lobby events by tournament code - Stub method"""
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
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(tournament_stub_v5_LobbyEventV5DTOWrapper).validate_python(response.json())
        
    
    async def register_provider_data(
        self,
        region: Union[Region, Platform, str],
        
        
        body: Optional[tournament_stub_v5_ProviderRegistrationParametersV5] = None,
        
    ) -> int:
        """Creates a tournament provider and returns its ID - Stub method"""
        path = "/lol/tournament-stub/v5/providers"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        kwargs: Dict[str, Any] = {"params": params}
        if body is not None:
            if hasattr(body, "model_dump"):
                kwargs["json"] = body.model_dump(by_alias=True, exclude_none=True)
            else:
                kwargs["json"] = body
        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            **kwargs
        )
        
        
        return TypeAdapter(int).validate_python(response.json())
        
    
    async def register_tournament(
        self,
        region: Union[Region, Platform, str],
        
        
        body: Optional[tournament_stub_v5_TournamentRegistrationParametersV5] = None,
        
    ) -> int:
        """Creates a tournament and returns its ID - Stub method"""
        path = "/lol/tournament-stub/v5/tournaments"
        # Replace path params
        

        # Query params
        params = {
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        kwargs: Dict[str, Any] = {"params": params}
        if body is not None:
            if hasattr(body, "model_dump"):
                kwargs["json"] = body.model_dump(by_alias=True, exclude_none=True)
            else:
                kwargs["json"] = body
        response = await self.http.request(
            method="POST",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            **kwargs
        )
        
        
        return TypeAdapter(int).validate_python(response.json())
        
    