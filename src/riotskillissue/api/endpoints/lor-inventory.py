# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Lor-inventoryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_cards(
        self,
        region: str,
        
    ) -> List[lor-inventory-v1.CardDto]:
        """
        Return a list of cards owned by the calling user.
        """
        path = "/lor/inventory/v1/cards/me"
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
    