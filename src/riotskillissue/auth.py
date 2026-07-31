from __future__ import annotations

import asyncio
import base64
import hashlib
import os
import secrets
import time
import urllib.parse
from dataclasses import dataclass, field
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Optional,
    Protocol,
    Tuple,
    Type,
    runtime_checkable,
)

import httpx

from riotskillissue.core.http import (
    MalformedResponseError,
    RiotAPIError,
    RiotNetworkError,
    RiotTimeoutError,
)


@dataclass(frozen=True)
class RsoConfig:
    client_id: str
    client_secret: str = field(repr=False)
    redirect_uri: str
    provider: str = "https://auth.riotgames.com"

    def __post_init__(self) -> None:
        if not self.client_id.strip() or not self.client_secret.strip():
            raise ValueError("RSO client credentials cannot be empty")
        if not self.redirect_uri.strip():
            raise ValueError("RSO redirect_uri cannot be empty")
        object.__setattr__(self, "provider", self.provider.rstrip("/"))


@dataclass(frozen=True)
class TokenResponse:
    access_token: str = field(repr=False)
    refresh_token: str = field(default="", repr=False)
    id_token: str = field(default="", repr=False)
    expires_in: int = 0
    scope: str = ""

    def __post_init__(self) -> None:
        if not self.access_token.strip():
            raise ValueError("RSO access token cannot be empty")
        if self.expires_in < 0:
            raise ValueError("expires_in cannot be negative")


@runtime_checkable
class RsoTokenProvider(Protocol):
    async def get_token(self) -> str:
        """Return a current RSO bearer token."""


@dataclass(frozen=True)
class StaticRsoTokenProvider:
    token: str = field(repr=False)

    def __post_init__(self) -> None:
        token = self.token.strip()
        if not token:
            raise ValueError("RSO access token cannot be empty")
        object.__setattr__(self, "token", token)

    async def get_token(self) -> str:
        return self.token


class RefreshingRsoTokenProvider:
    def __init__(
        self,
        tokens: TokenResponse,
        refresh: Callable[[str], Awaitable[TokenResponse]],
        *,
        refresh_leeway: float = 30.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if refresh_leeway < 0:
            raise ValueError("refresh_leeway cannot be negative")
        self._tokens = tokens
        self._refresh = refresh
        self._refresh_leeway = refresh_leeway
        self._clock = clock
        self._expires_at = clock() + tokens.expires_in
        self._lock = asyncio.Lock()

    def __repr__(self) -> str:
        return "<RefreshingRsoTokenProvider>"

    def _is_current(self) -> bool:
        return self._clock() < self._expires_at - self._refresh_leeway

    async def get_token(self) -> str:
        if self._is_current():
            return self._tokens.access_token
        async with self._lock:
            if self._is_current():
                return self._tokens.access_token
            if not self._tokens.refresh_token:
                raise ValueError("RSO refresh token is unavailable")
            previous = self._tokens
            refreshed = await self._refresh(previous.refresh_token)
            self._tokens = TokenResponse(
                access_token=refreshed.access_token,
                refresh_token=refreshed.refresh_token or previous.refresh_token,
                id_token=refreshed.id_token or previous.id_token,
                expires_in=refreshed.expires_in,
                scope=refreshed.scope or previous.scope,
            )
            self._expires_at = self._clock() + self._tokens.expires_in
            return self._tokens.access_token


def _generate_pkce() -> Tuple[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("ascii")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def _token_error_message(response: httpx.Response) -> str:
    message = "RSO token request failed"
    try:
        payload = response.json()
    except ValueError:
        return message
    if not isinstance(payload, dict):
        return message
    error = payload.get("error")
    if (
        isinstance(error, str)
        and 0 < len(error) <= 64
        and all(character.isalnum() or character in "._-" for character in error)
    ):
        return error
    return message


def _parse_tokens(
    response: httpx.Response, previous: Optional[TokenResponse] = None
) -> TokenResponse:
    try:
        payload: Any = response.json()
    except ValueError as exc:
        raise MalformedResponseError(
            "RSO token endpoint returned malformed JSON", response=response
        ) from exc
    if not isinstance(payload, dict):
        raise MalformedResponseError(
            "RSO token endpoint returned a non-object response", response=response
        )
    try:
        access_token = payload["access_token"]
        refresh_token = payload.get("refresh_token")
        id_token = payload.get("id_token")
        scope = payload.get("scope")
        if not isinstance(access_token, str):
            raise TypeError
        if refresh_token is not None and not isinstance(refresh_token, str):
            raise TypeError
        if id_token is not None and not isinstance(id_token, str):
            raise TypeError
        if scope is not None and not isinstance(scope, str):
            raise TypeError
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
            or (previous.refresh_token if previous else ""),
            id_token=id_token or (previous.id_token if previous else ""),
            expires_in=int(payload.get("expires_in", 0)),
            scope=scope or (previous.scope if previous else ""),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise MalformedResponseError(
            "RSO token endpoint returned an invalid token response", response=response
        ) from exc


class RsoClient:
    def __init__(self, config: RsoConfig):
        self.config = config
        self.http = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0, connect=5.0, write=10.0, pool=5.0)
        )

    async def close(self) -> None:
        await self.http.aclose()

    async def __aenter__(self) -> "RsoClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    def get_auth_url(
        self,
        scope: str = "openid",
        *,
        use_pkce: bool = True,
    ) -> Dict[str, str]:
        state = secrets.token_urlsafe(32)
        params: Dict[str, str] = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
        }
        result: Dict[str, str] = {"state": state}

        if use_pkce:
            verifier, challenge = _generate_pkce()
            params["code_challenge"] = challenge
            params["code_challenge_method"] = "S256"
            result["code_verifier"] = verifier

        result["url"] = (
            f"{self.config.provider}/authorize?{urllib.parse.urlencode(params)}"
        )
        return result

    async def _request_tokens(
        self, data: Dict[str, str], previous: Optional[TokenResponse] = None
    ) -> TokenResponse:
        try:
            response = await self.http.post(
                f"{self.config.provider}/token",
                auth=(self.config.client_id, self.config.client_secret),
                data=data,
            )
        except httpx.TimeoutException as exc:
            raise RiotTimeoutError("RSO token request timed out") from exc
        except (httpx.NetworkError, httpx.RemoteProtocolError) as exc:
            raise RiotNetworkError("RSO token request failed") from exc

        if not response.is_success:
            raise RiotAPIError(
                response.status_code, _token_error_message(response), response
            )
        return _parse_tokens(response, previous)

    async def exchange_code(
        self,
        code: str,
        *,
        code_verifier: Optional[str] = None,
    ) -> TokenResponse:
        data: Dict[str, str] = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
        }
        if code_verifier:
            data["code_verifier"] = code_verifier
        return await self._request_tokens(data)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        return await self._request_tokens(
            {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        )

    def create_token_provider(
        self,
        tokens: TokenResponse,
        *,
        refresh_leeway: float = 30.0,
    ) -> RefreshingRsoTokenProvider:
        return RefreshingRsoTokenProvider(
            tokens,
            self.refresh_token,
            refresh_leeway=refresh_leeway,
        )

    async def exchange_code_for_provider(
        self,
        code: str,
        *,
        code_verifier: Optional[str] = None,
        refresh_leeway: float = 30.0,
    ) -> RefreshingRsoTokenProvider:
        tokens = await self.exchange_code(code, code_verifier=code_verifier)
        return self.create_token_provider(tokens, refresh_leeway=refresh_leeway)
