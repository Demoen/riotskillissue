# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riot.core.http import HttpClient
from riot.core.types import Region, Platform
from riot.api.models import *

class Lol-statusApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_platform_data(
        self,
        region: str,
        
    ) -> lol-status-v4.PlatformDataDto:
        """
        Get League of Legends status for the given platform.
        """
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
            region_or_platform=region,
            params=params
        )
        return response.json()
    