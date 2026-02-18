# Generated Code. Do not edit.
from __future__ import annotations
from typing import Optional, Union, List, Dict, Any
from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import Region, Platform
from riotskillissue.api.models import *

class RiftboundContentApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_content(
        self,
        region: Union[Region, Platform, str],
        
        locale: str = None,
        
        
    ) -> riftbound_content_v1_RiftboundContentDTO:
        """Get riftbound content"""
        path = "/riftbound/content/v1/contents"
        # Replace path params
        

        # Query params
        params = {
            
            "locale": locale,
            
        }
        # Filter None
        params = {k: v for k, v in params.items() if v is not None}

        
        response = await self.http.request(
            method="GET",
            url=path,
            region_or_platform=region.value if hasattr(region, "value") else str(region),
            params=params
        )
        
        
        return TypeAdapter(riftbound_content_v1_RiftboundContentDTO).validate_python(response.json())
        
    