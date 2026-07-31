# VALORANT

```python
async with RiotClient(default_route=ValorantRoute.EU) as riot:
    profile = await riot.valorant.profile("Player#EUW")
    history = await riot.valorant.match_history("Player#EUW", count=5)
    leaderboard = await riot.valorant.leaderboard(
        act_id="00000000-0000-0000-0000-000000000000",
        size=20,
    )
```

Use `riot.raw.valorant` for the complete generated VALORANT API.
