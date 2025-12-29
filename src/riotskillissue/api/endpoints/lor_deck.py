# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Lor_deckApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_decks(
        self,
        region: str,
        
    ) -> List[lor_deck_v1_DeckDto]:
        """
        Get a list of the calling user's decks.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[lor_deck_v1_DeckDto]).validate_python(response.json())
        
    
    async def create_deck(
        self,
        region: str,
        
    ) -> str:
        """
        Create a new deck for the calling user.
        """
        path = "/lor/deck/v1/decks/me"
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
        return TypeAdapter(str).validate_python(response.json())
        
    