# Production readiness review — 2026-09-06

## Source and release status

The SDK updater is active and the bundled schema matches its live upstream feed.
The feed is a community-maintained conversion of Riot's API reference, not an
official Riot OpenAPI contract. Matching it does not independently prove every
live Riot endpoint or response matches the documentation.

| Check | Evidence |
|---|---|
| Repository updater | [September 6 run](https://github.com/Demoen/riotskillissue/actions/runs/34000617404) succeeded at 00:11 UTC; fetched the feed and found no changes. |
| Upstream generator | [September 6 run](https://github.com/MingweiSamuel/riotapi-schema/actions/runs/34003448701) succeeded at 01:16 UTC; regenerated without a content change. |
| Last schema modification | [August 5 schema commit](https://github.com/MingweiSamuel/riotapi-schema/commit/f4d8f45a9da40770a0c131a92ccfcd764c9081e8). The old content date does not mean the generator stopped. |
| Local/live parity | 78 paths, 80 operations, 180 schemas; SHA-256 of sorted JSON: `ab5facfd5403aa8e7edcc44448a9ac0ef1a4ce38d099e507572b84ec134778f6`. |
| Published package | [PyPI](https://pypi.org/project/riotskillissue/1.1.0/) still distributes 1.1.0, while [GitHub has v1.1.1](https://github.com/Demoen/riotskillissue/releases/tag/v1.1.1). |

The v1.1.1 updater created its tag and GitHub release on August 10 before the
[explicit Publish workflow dispatch fix](https://github.com/Demoen/riotskillissue/commit/a897ff27a9ff069067a2b491518d42a1cedaf90b)
was added. No Publish run followed that tag. Its tagged workflow does not contain
the later dispatch support, so recovery should use a reviewed new release/tag
containing the fixed workflow. This review did not publish a package or push changes.

## Implemented improvements

- Source checks now validate the downloaded document before replacing the bundled
  schema and replace it atomically. Connection retries and an explicit timeout
  make fetching less fragile.
- `python tools/manager.py --check --check-upstream` checks drift without modifying
  the repository. It reports provenance and requires a successful upstream
  scheduled run in the last 72 hours. Every successful check emits a CI summary,
  including checks that find no changes.
- Structural diff reports cover nested model fields, parameter types and locations,
  references, request bodies, responses, authentication, routing, and metadata.
  The old report could say "No Significant Changes" for real contract changes.
- The updater runs at 03:17 UTC, after upstream's usual generation, serializes
  concurrent update jobs, checks new as well as tracked generated files, and
  verifies the SDK even on unchanged days. Branch and tag pushes are atomic.
- CI installs the Redis and TUI extras and adds Windows test jobs alongside Linux.
- Ambiguous POST/PATCH transport and server failures are no longer automatically
  replayed. Failures before sending and explicit rate-limit rejection remain
  retryable; idempotent requests retain transient retries.
- Redis cache entries have their own namespace. Clearing the cache preserves
  other application data and rate-limit counters. Serialization preserves
  integer dictionary keys used by Data Dragon maps.
- HTTP shutdown closes internally created rate limiters, including when HTTP
  connection cleanup fails. Callers retain ownership of injected limiters.
- TUI refreshes run in background workers, preserve keyboard responsiveness,
  suppress overlapping refreshes, and reuse one client across refreshes.
  Countdown text updates continuously. Failed enrichment retains players with
  warnings; failed refreshes retain the previous snapshot with a stale indicator.
  Shutdown cancels requests before closing the client.
- MCP initialization advertises the installed package version.
- Four generated placeholder models preserve undocumented response fields,
  including nested RSO match data and console leaderboard tiers. Previously,
  Pydantic silently discarded their payloads. Concrete model validation is unchanged.

## Remaining priorities

| Priority | Work | Reason |
|---|---|---|
| High | Publish a reviewed new version containing the release dispatch fix and these changes. | GitHub release availability and PyPI package availability currently differ. |
| High | Reconcile Redis rate limits with Riot's response counts; add real Redis integration tests with multiple clients. | `RedisRateLimiter.update()` is still a no-op. Local acquisitions alone cannot account for all observed usage. |
| High | Return explicit partial-result diagnostics from high-level match-history workflows. | `_match_summaries` discards failed match requests, so a complete downstream outage can look like empty history. |
| High | Classify breaking SDK changes and route automatic updates through reviewed releases. | Structural reports are not compatibility analysis; the updater still always increments the patch version. Endpoint removal or required-argument changes can require a major release. |
| Medium | Add a shared CLI/MCP diagnostics surface and optional request metrics. | Source provenance, route selection, credential presence, cache hits, retries, and rate-limit wait time would make support and operations easier. Credentials must remain redacted. |
| Medium | Automate review of the MCP mechanics knowledge by patch. | The handwritten economy registry is verified only through public patch 26.15. SDK schema generation does not update game-mechanics knowledge. |
| Medium | Add opt-in authenticated smoke tests and packaged-install checks across supported runtimes. | Mocked API tests cannot prove live key entitlements, routing behavior, or undocumented Riot response changes. |

## Validation

On Windows with Python 3.14.5 and the current allowed dependencies:

- 218 tests passed, including Redis behavior tests with a stub and headless TUI tests.
- Ruff passed; mypy passed for 114 source files.
- Actionlint passed for the GitHub workflows.
- Generation parity passed for 81 managed files.
- Strict documentation build passed with the workspace's Zensical configuration.
- Wheel and source distribution builds passed.
- The wheel installed into a separate environment without optional extras;
  imports, CLI help, async/sync client lifecycles, and placeholder payload
  preservation passed there.
- The source health command passed against the live community feed and GitHub API.

No authenticated Riot requests, live Redis integration tests, hosted runs of the
modified workflows, or local Python 3.15/3.16 tests were performed. The existing
Python 3.12 virtual environment was preserved; validation used an isolated
Python 3.14 environment under `.tmp_tests/`.
