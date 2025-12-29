from typing import Optional, Type, TypeVar
from types import TracebackType

from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.http import HttpClient

from riotskillissue.api.client_mixin import GeneratedClientMixin

from riotskillissue.core.cache import AbstractCache

class RiotClient(GeneratedClientMixin):
    """
    Main entry point for the Riot Games API.
    
    Usage:
        async with RiotClient(api_key="...") as client:
            client.summoner.get_by_name(...)
    """
    def __init__(self, api_key: Optional[str] = None, config: Optional[RiotClientConfig] = None, cache: Optional[AbstractCache] = None, hooks: Optional[dict] = None):
        if config is None:
            if api_key:
                # Create config from key
                config = RiotClientConfig(api_key=api_key)
            else:
                # Load from env
                config = RiotClientConfig.from_env()
        
        self.config = config
        self.http = HttpClient(config, cache=cache, hooks=hooks)
        
        # Static Data
        from riotskillissue.static import DataDragonClient
        self.static = DataDragonClient(cache=cache)
        
        # Initialize generated APIs
        super().__init__(self.http)
        
    async def __aenter__(self) -> "RiotClient":
        return self

    async def __aexit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_val: Optional[BaseException], 
        exc_tb: Optional[TracebackType]
    ) -> None:
        await self.http.close()
