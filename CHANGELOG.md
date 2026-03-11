# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-11

### ⚠️ Breaking Changes
- **Python**: Minimum Python version raised from 3.8 to **3.10**. Python 3.8 and 3.9 are no longer supported.
- **Dependencies**: `redis` and `textual` moved from core dependencies to optional extras. Install with `pip install riotskillissue[redis]` or `pip install riotskillissue[tui]`.
- **Dependencies**: `frozendict` and `msgspec` removed from dependencies entirely.
- **Cache**: `RedisCache` serialization switched from `pickle` to JSON + base64. Existing cached entries in Redis are **incompatible** and should be flushed after upgrading.
- **Errors**: `ServerError` constructor simplified to `ServerError(response)` (previously took `status_code, message, response`).

### Added
- **Typing**: Added `py.typed` marker file (PEP 561) for downstream type-checking support.
- **Exports**: Top-level package now exports `AbstractRateLimiter`, `MemoryRateLimiter`, `gather_limited`, `DataDragonClient`, `RsoClient`, `RsoConfig`, `TokenResponse`. `RedisCache` and `RedisRateLimiter` are exported when the `redis` extra is installed.
- **Context Managers**: `RsoClient` and `DataDragonClient` now support `async with` for automatic resource cleanup.
- **Dependencies**: New `[redis]` and `[tui]` optional dependency groups.

### Changed
- **Rate Limiting**: `MemoryRateLimiter` now releases its lock while sleeping, allowing requests on other keys to proceed concurrently.
- **Pagination**: `paginate()` `max_results` parameter changed from `float('inf')` default to `None` (no functional change for callers).
- **Sync Client**: Uses `inspect.iscoroutinefunction` instead of `asyncio.iscoroutinefunction` for more reliable coroutine detection. Replaced bare `assert` with `RuntimeError` for missing event loop.
- **Code Generation**: Endpoint template now wraps optional parameters in `Optional[...]` for correct type annotations.
- **CI**: Added dedicated lint job (ruff + mypy). Added pip caching. Removed Python 3.8/3.9 from test matrix, kept 3.14.
- **Tooling**: Added mypy overrides to exclude auto-generated code and suppress known false positives. Configured ruff exclusions and per-file ignores for generated files.

### Fixed
- **Rate Limiting**: `MemoryRateLimiter.acquire()` now re-checks limits after sleeping, preventing burst requests from slipping through when multiple callers wait simultaneously.
- **Cache Security**: `RedisCache` no longer uses `pickle` for serialization, eliminating the risk of arbitrary code execution from tampered cache entries.

## [0.2.2] - 2026-02-23

### Added
- **Models**: New `match_v5_ParticipantPlayerBehaviorDto` model with `PlayerBehavior_IsHeroInCombat` field, added to `match_v5_ParticipantDto.PlayerBehavior`.

## [0.2.1] - 2026-02-18

### Fixed
- **HTTP**: Added `Accept-Encoding: identity` header to `HttpClient` to prevent `zlib-ng` decompression errors on Python 3.13+/3.14. The new `zlib-ng` backend shipped with these versions can fail with "Error -3 while decompressing data: incorrect header check" on certain Riot API gzip/deflate responses, breaking endpoints that return large payloads (match timelines, heatmaps, etc.).

## [0.2.0] - 2026-02-18

### ⚠️ Breaking Changes
- **Auth**: `RSOClient.get_auth_url()` now returns a `dict` with keys `url`, `state`, and `code_verifier` instead of a plain URL string. This enables PKCE and CSRF protection.
- **Error Handling**: HTTP 429 responses are no longer raised as `RateLimitError` immediately. The client now automatically sleeps for the `Retry-After` duration and retries the request transparently.
- **Errors**: The exception hierarchy has changed. Import specific error classes from the top-level package (`BadRequestError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`, `RateLimitError`, `ServerError`).

### Added
- **Sync Client**: New `SyncRiotClient` — a fully synchronous wrapper around `RiotClient`. Use it from scripts, notebooks, or any non-async context with the same API surface.
  ```python
  from riotskillissue import SyncRiotClient

  with SyncRiotClient(api_key="RGAPI-...") as client:
      account = client.account.get_by_riot_id(region="americas", gameName="Faker", tagLine="KR1")
  ```
- **Error Hierarchy**: Granular, typed exception classes — `BadRequestError` (400), `UnauthorizedError` (401), `ForbiddenError` (403), `NotFoundError` (404), `RateLimitError` (429), `ServerError` (5xx). All inherit from `RiotAPIError`.
- **PKCE & CSRF**: RSO OAuth2 flow now generates PKCE `code_verifier`/`code_challenge` and a random `state` parameter automatically.
- **Config**: New `RiotClientConfig` fields: `cache_ttl`, `proxy`, `base_url`, `log_level`.
- **Config**: `RiotClientConfig.from_env()` now reads `RIOT_CACHE_TTL`, `RIOT_PROXY`, `RIOT_BASE_URL`, `RIOT_LOG_LEVEL` from the environment.
- **Cache**: `MemoryCache` now supports LRU eviction with configurable `max_size` (default 1024).
- **Cache**: `AbstractCache` gained `delete()` and `clear()` methods.
- **Static Data**: `DataDragonClient` expanded with `get_summoner_spells()`, `get_summoner_spell()`, `get_runes()`, `get_queues()`, `get_maps()`, `get_game_modes()`.
- **Exports**: Top-level package now exports `__version__`, `SyncRiotClient`, all error classes, and cache classes.
- **Logging**: Structured logging with configurable log level via `RiotClientConfig(log_level="DEBUG")`.
- **Proxy**: HTTP proxy support via `RiotClientConfig(proxy="http://127.0.0.1:8080")`.
- **Base URL Override**: `RiotClientConfig(base_url="...")` for custom API endpoints or testing.
- **Client**: `RiotClient` now has a `close()` method and `__repr__` with masked API key.

### Changed
- **Rate Limiting**: Rate limiter is now properly wired into every request. `acquire()` is called before each API call.
- **429 Handling**: HTTP 429 responses are automatically retried after sleeping for the `Retry-After` header value. These retries do not count against `max_retries`.
- **Retries**: Uses `config.max_retries` instead of hardcoded 3 for 5xx/network error retry attempts.
- **Cache TTL**: Uses `config.cache_ttl` instead of hardcoded 60 seconds.
- **Data Dragon**: `DataDragonClient` is now lazily initialized (not created until first access via `client.static`).
- **Resource Cleanup**: All HTTP clients (`RiotClient`, `DataDragonClient`, `RSOClient`) now properly close their underlying `httpx.AsyncClient` on exit.

### Fixed
- **Duplicate Endpoints**: Removed 23 duplicate hyphenated endpoint files (e.g. `champion-mastery.py` alongside `champion_mastery.py`).
- **Rate Limit Headers**: Response rate-limit headers are now parsed and used to dynamically update internal limits.

### Code Generation Improvements
- **Models**: Required vs optional fields are now correctly distinguished (`Field(alias=...)` without default for required, `Field(default=None, alias=...)` for optional).
- **Models**: Enum schemas generate `Literal[...]` type aliases instead of empty `BaseModel` classes.
- **Models**: All models include `model_config = {"populate_by_name": True}` and `model_rebuild()` calls.
- **Endpoints**: `TypeAdapter` is imported at module level (not per-method).
- **Endpoints**: `region` parameter is typed as `Union[Region, Platform, str]`.
- **Endpoints**: POST/PUT endpoints support request body parameters.
- **Generator**: Output directory is cleaned before regeneration, preventing stale duplicate files.

## [0.1.5] - 2026-02-08
### Changed
- **API**: Updated Riot API Spec (automated update).
- **CI/CD**: Fixed `update-sdk` workflow to correctly handle version tagging and deprecated commands.

## [0.1.4] - 2026-02-06
### Added
- **TUI**: Initial Terminal User Interface functionality for monitoring and interaction.

### Changed
- **License**: Switched project license to MIT License.

## [0.1.3] - 2026-02-03
### Added
- **Documentation**: Complete MkDocs Material documentation site with LoL-inspired theme.
- **Documentation**: Getting Started, Configuration, API Reference, and CLI guides.
- **Documentation**: Comprehensive examples for LoL, TFT, and VALORANT APIs.
- **Examples**: Runnable example scripts (`basic_usage.py`, `match_history.py`, `champion_mastery.py`).

### Changed
- **README**: Rewritten for professional presentation.
- **Dependencies**: Added `docs` optional dependency group for MkDocs.

## [0.1.2] - 2026-01-27
### Changed
- **API**: Update Riot API Spec (automated update via GitHub Actions).

## [0.1.1] - 2025-12-29
### Changed
- **API**: Update Riot API Spec (automated update via GitHub Actions).

## [0.1.0] - 2025-12-29
### Added
- Initial release of `riotskillissue`.
- **Core**: Resilient `RiotClient` with `HttpClient`, `RedisCache`, and `RedisRateLimiter`.
- **API**: Full coverage for League of Legends, TFT, LoR, and VALORANT (generated from Spec).
- **CLI**: `riotskillissue-cli` for quick lookups and debugging.
- **Auth**: Riot Sign-On (RSO) OAuth2 helper.
- **Pagination**: Async iterator `paginate()` for paginated endpoints.
- **Static**: `DataDragonClient` for fetching versions and assets.
