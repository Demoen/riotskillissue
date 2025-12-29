# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-29
### Added
- Initial release of `riotskillissue`.
- **Core**: Resilient `RiotClient` with `HttpClient`, `RedisCache`, and `RedisRateLimiter`.
- **API**: Full coverage for League of Legends, TFT, LoR, and VALORANT (generated from Spec).
- **CLI**: `riotskillissue-cli` for quick lookups and debugging.
- **Auth**: Riot Sign-On (RSO) OAuth2 helper.
- **Pagination**: Async iterator `paginate()` for paginated endpoints.
- **Static**: `DataDragonClient` for fetching versions and assets.
