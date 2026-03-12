# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class LorDeckApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_decks(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> List[lor_deck_v1_DeckDto]:
        """Get a list of the calling user's decks."""
        path = "/lor/deck/v1/decks/me"
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
        
        
        return TypeAdapter(List[lor_deck_v1_DeckDto]).validate_python(response.json())
        
    
    async def create_deck(
        self,
        region: Union[Region, Platform, str],
        
        
        body: Optional[lor_deck_v1_NewDeckDto] = None,
        
    ) -> str:
        """Create a new deck for the calling user."""
        path = "/lor/deck/v1/decks/me"
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
        
        
        return TypeAdapter(str).validate_python(response.json())
        
    