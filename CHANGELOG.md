# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
