# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Lor_statusApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_platform_data(
        self,
        region: str,
        
    ) -> lor_status_v1_PlatformDataDto:
        """
        Get Legends of Runeterra status for the given platform.
        """
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(lor_status_v1_PlatformDataDto).validate_python(response.json())
        
    