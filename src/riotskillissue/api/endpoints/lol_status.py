# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class LolStatusApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_platform_data(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> lol_status_v4_PlatformDataDto:
        """Get League of Legends status for the given platform."""
        path = "/lol/status/v4/platform-data"
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
        
        
        return TypeAdapter(lol_status_v4_PlatformDataDto).validate_python(response.json())
        
    