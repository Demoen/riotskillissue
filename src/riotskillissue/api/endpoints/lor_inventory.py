# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Lor_inventoryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_cards(
        self,
        region: str,
        
    ) -> List[lor_inventory_v1_CardDto]:
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
        
        from pydantic import TypeAdapter
        return TypeAdapter(List[lor_inventory_v1_CardDto]).validate_python(response.json())
        
    