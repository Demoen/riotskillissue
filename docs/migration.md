# Migrating from 0.3 to 1.0

Version 1.0 is a clean break. There are no runtime compatibility aliases.

## Client layout

Flat endpoint namespaces moved below `raw` and are grouped by game and service.

```python
# 0.3
await riot.match.get_match(region="europe", matchId=match_id)

# 1.0
await riot.raw.lol.match.get_match(match_id=match_id)
```

Common tasks now use game workflows:

```python
profile = await riot.lol.player_profile("Player#EUW")
history = await riot.lol.match_history("Player#EUW", count=5)
```

## Names and routes

- Camel-case endpoint parameters became keyword-only snake_case.
- `Region` and `Platform` were replaced by `PlatformRoute`,
  `RegionalRoute`, and `ValorantRoute`.
- Supply `default_route=` when constructing a client, or pass `route=` to a
  call that cannot be inferred.
- Generated model identifiers moved to stable service modules. Fields use
  snake_case and retain Riot wire names as Pydantic aliases.

```python
python_names = match.model_dump()
riot_wire_names = match.model_dump(by_alias=True)
```

## Sync

`SyncRiotClient` now has explicit typed workflow and raw methods. Public
endpoint access no longer depends on dynamic attribute forwarding.

## RSO

Bearer tokens are supplied through an `RsoTokenProvider` on the client. Remove
token arguments from endpoint calls. RSO responses are uncached by default.
