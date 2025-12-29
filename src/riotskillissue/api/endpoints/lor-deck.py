# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Lor-deckApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_decks(
        self,
        region: str,
        
    ) -> List[lor-deck-v1.DeckDto]:
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
        return response.json()
    
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
        return response.json()
    