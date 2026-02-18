# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class LorStatusApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_platform_data(
        self,
        region: Union[Region, Platform, str],
        
        
    ) -> lor_status_v1_PlatformDataDto:
        """Get Legends of Runeterra status for the given platform."""
        path = "/lor/status/v1/platform-data"
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
        
        
        return TypeAdapter(lor_status_v1_PlatformDataDto).validate_python(response.json())
        
    