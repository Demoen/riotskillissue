# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2026-09-06

### Added

- A read-only schema health command: `python tools/manager.py --check --check-upstream`.
  Reports the source hash, API coverage, and latest successful upstream generation;
  detects schema drift and generators with no successful run in 72 hours.
- Live-game TUI diagnostics for unavailable champion/rank data and failed refreshes,
  retaining the last successful snapshot with a visible stale-data indicator.
- Windows CI coverage alongside Linux, with Redis and TUI extras installed.

### Changed

- Scheduled SDK checks run after upstream generation and verify tests, typing,
  lint, generated code, documentation, and packaging even when the schema is unchanged.
- Schema reports cover nested fields, parameters, responses, request bodies,
  authentication, routing, and metadata. Downloads are validated before atomic replacement.
- TUI refreshes run in background workers and reuse one client, retaining
  connections, static-data cache, and learned rate limits between requests.
- Documentation builds and publishing use Zensical, preserving the existing
  theme, navigation, and page URLs.

### Fixed

- Prevented automatic replay of POST/PATCH requests after ambiguous transport
  failures or server errors, avoiding duplicate mutations. Connection failures
  before sending and explicit rate-limit rejections remain retryable.
- Redis cache clearing now removes only namespaced cache entries, preserving
  rate-limit counters and unrelated application data. Cached maps retain integer keys.
- Internally created rate-limit connections close with the HTTP client, including
  when HTTP cleanup fails; injected limiters remain owned by the caller.
- Required Redis 5.0.1 or newer for its asynchronous connection cleanup API.
- Kept TUI keyboard controls responsive during requests, prevented overlapping
  refreshes, updated countdown text, and cancelled pending requests on exit.
- Preserved players after optional data lookup failures and distinguished an
  unknown account from a player who is not currently in a game.
- Preserved undocumented response fields in generated placeholder models,
  including RSO matches/timelines and console leaderboard tiers.
- MCP initialization reports the installed package version.
- Release publishing validates the tag against package metadata and reviewed
  changelog notes. GitHub releases are created only after successful PyPI publication.

### Upgrade notes

- Existing Redis cache entries are not reused after the namespace change and
  expire according to their original TTL. Expect a one-time cold cache.
- Callers of POST/PATCH operations must handle ambiguous failures explicitly;
  retrying those operations can duplicate a write that Riot already accepted.
- Programmatic TUI refresh intervals must be at least five seconds, matching the CLI.
- Python requirements remain `>=3.14,<3.17`. The TUI, MCP, and Redis remain optional extras.

## [1.1.1] - 2026-08-10

### Changed

- Synchronized the bundled community Riot API schema. This version was released
  on GitHub but was not published to PyPI.

## [1.1.0] - 2026-08-02

This is a major League intelligence upgrade for the MCP server. It now turns
Riot match, timeline, player, and patch data into evidence-backed context for
natural-language game analysis instead of returning disconnected API payloads.

### Added

- League-first `riot_lol_match_context`, `riot_lol_player_context`,
  `riot_lol_knowledge`, and `riot_lol_item_economy` tools.
- Match V5 timeline analysis covering participants, lane comparisons, gold/XP/CS
  checkpoints, item timings, likely fights, objectives, nearby trades, and later
  structure conversion.
- Evidence-qualified Void Grub impact analysis with capture timing, direct
  rewards, bounded conversion signals, long-horizon context, and explicit causal
  limits.
- Combined player context for Riot identity, summoner profile, ranked entries,
  mastery, challenges, recent matches, and bounded performance aggregation.
- Patch-banded standard Summoner's Rift fundamentals for minion-wave gold and
  XP, shared experience, wave schedules, passive income, role modifiers,
  structures, neutral objectives, and strategic opportunity cost.
- Patch-matched item raw-stat efficiency derived from Data Dragon component
  prices, including per-stat formulas, coverage, map applicability, and explicit
  reporting for effects that cannot be priced safely.
- Strict patch and locale selection for League game content, public-to-internal
  patch normalization, full champion ability payloads, and automatically
  refreshing Data Dragon version discovery.
- Configurable per-result and aggregate MCP memory ceilings with bounded,
  in-memory paginated result handles.

### Changed

- MCP instructions now route League questions through the relevant match,
  player, mechanics, economy, and static-content evidence sources.
- Optional upstream failures are surfaced through warnings, unavailable
  sections, telemetry completeness, and source provenance instead of silently
  changing the analysis scope.
- Compact player output omits PUUIDs and distinguishes requested, loaded,
  analyzed, and returned recent-match counts.
- Objective conversion uses actual timeline timestamps and bounded post-capture
  windows; whole-match outcomes are retained as unscored context.

### Fixed

- Historical match enrichment now rejects cross-patch Data Dragon fallback
  instead of attaching current item, rune, or spell data to an older match.
- Corrected SEA Account V1 routing while preserving Match V5 regional routing.
- Tightened required match payload validation, partial timeline handling,
  deterministic UTC timestamps, public/internal patch normalization, and
  Swiftplay-specific Void Grub applicability.
- Prevented missing objective telemetry from being reported as a proven zero and
  prevented unsupported item effects from being reported as zero value.

### Security

- MCP operation authentication now fails closed for unknown modes and exposes
  only API-key or unauthenticated operations.
- Credentials remain environment-only, RSO operations remain hidden from the
  public MCP gateway, and writes remain disabled unless explicitly enabled and
  confirmed.

## [1.0.0] - 2026-07-31

### Breaking

- Raised the required Python version to `>=3.14,<3.17`, covering Python 3.14,
  3.15, and 3.16. Release verification covers Python 3.14 and the current 3.15
  prerelease, with a non-blocking CPython 3.16 nightly compatibility probe.
- Replaced the flat endpoint surface with game workflows and the generated
  `client.raw.<game>.<service>` hierarchy.
- Replaced `Region` and `Platform` with `PlatformRoute`, `RegionalRoute`, and
  `ValorantRoute`.
- Changed generated parameters and model fields to snake_case and moved models
  into stable service modules.
- Removed runtime 0.3 compatibility aliases.

### Added

- Focused workflows for League of Legends, TFT, VALORANT, Legends of Runeterra,
  and Riftbound.
- An explicit typed `SyncRiotClient` surface.
- A committed operation registry shared by generated clients, documentation,
  validation, and MCP discovery.
- An optional local stdio MCP server with high-level tools, exhaustive eligible
  read discovery, confirmed opt-in writes, and bounded in-memory result handles.
- Typed route, credential, network, timeout, malformed-response, validation, and
  rate-limit failures.
- Static and automatically refreshing RSO token providers.

### Fixed

- Security-metadata-driven API-key and bearer authentication.
- Bounded HTTP 429 retries, strict `Retry-After` parsing, independent Riot
  rate-limit buckets, cancellation propagation, and all 2xx/no-content handling.
- Credential-partitioned caching and cache-disabled RSO defaults.
- CLI routing, configuration parsing, generated-code typing, and stale examples.

## [0.3.3] - 2026-07-22

### Changed

- Synced latest Riot API spec

## [0.3.2] - 2026-03-12

### Changed

- Synced latest Riot API spec

## [0.3.1] - 2026-03-11

### Fixed
- **Documentation**: Updated installation instructions to reflect `redis` and `textual` as optional extras (`[redis]`, `[tui]`).
- **Documentation**: Updated "What's New" section from v0.2.0 to v0.3.0 with breaking changes warning.
- **Documentation**: Added Redis cache migration note for pickle → JSON+base64 serialization change.
- **Documentation**: Fixed CLI docs referencing `[dev]` extras instead of `[tui]` for live game TUI.

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

[1.1.2]: https://github.com/Demoen/riotskillissue/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/Demoen/riotskillissue/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/Demoen/riotskillissue/compare/v1.0.0...v1.1.0
