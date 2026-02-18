# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class LorInventoryApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_cards(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> List[lor_inventory_v1_CardDto]:
        """Return a list of cards owned by the calling user."""
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
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(List[lor_inventory_v1_CardDto]).validate_python(response.json())
        
    