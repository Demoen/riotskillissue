import os
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class RiotClientConfig:
    api_key: str
    redis_url: Optional[str] = None
    max_retries: int = 3
    connect_timeout: float = 5.0
    read_timeout: float = 10.0
    
    @classmethod
    def from_env(cls) -> "RiotClientConfig":
        return cls(
            api_key=os.environ.get("RIOT_API_KEY", ""),
            redis_url=os.environ.get("RIOT_REDIS_URL"),
            max_retries=int(os.environ.get("RIOT_MAX_RETRIES", "3")),
        )
