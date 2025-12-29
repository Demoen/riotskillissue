# Generated Code. Do not edit.
from typing import Optional, List, Dict, Any
from riotskillissue.core.http import HttpClient
from riotskillissue.api.models import *

class Val_contentApi:
    def __init__(self, http: HttpClient):
        self.http = http

    
    async def get_content(
        self,
        region: str,
        
        locale: str = None,
        
    ) -> val_content_v1_ContentDto:
        """
        Get content optionally filtered by locale
        """
        path = "/val/content/v1/contents"
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
            region_or_platform=region,
            params=params
        )
        
        from pydantic import TypeAdapter
        return TypeAdapter(val_content_v1_ContentDto).validate_python(response.json())
        
    