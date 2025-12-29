from typing import Optional, Dict, Any
from dataclasses import dataclass
import httpx
from riotskillissue.core.http import RiotAPIError

@dataclass
class RsoConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    provider: str = "https://auth.riotgames.com"

@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int
    scope: str

class RsoClient:
    """
    Helper for Riot Sign-On (OAuth2).
    """
    def __init__(self, config: RsoConfig):
        self.config = config
        self.http = httpx.AsyncClient()

    def get_auth_url(self, scope: str = "openid") -> str:
        """Generating the login URL for the user."""
        base = f"{self.config.provider}/authorize"
        return (
            f"{base}?client_id={self.config.client_id}"
            f"&redirect_uri={self.config.redirect_uri}"
            f"&response_type=code"
            f"&scope={scope}"
        )

    async def exchange_code(self, code: str) -> TokenResponse:
        """Exchange the auth code for tokens."""
        url = f"{self.config.provider}/token"
        
        resp = await self.http.post(
            url,
            auth=(self.config.client_id, self.config.client_secret),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.config.redirect_uri,
            }
        )
        
        if not resp.is_success:
            raise RiotAPIError(resp.status_code, resp.text, resp)
            
        data = resp.json()
        return TokenResponse(**data)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Get new access token using refresh token."""
        url = f"{self.config.provider}/token"
        
        resp = await self.http.post(
            url,
            auth=(self.config.client_id, self.config.client_secret),
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        )
        
        if not resp.is_success:
            raise RiotAPIError(resp.status_code, resp.text, resp)
            
        data = resp.json()
        return TokenResponse(**data)
