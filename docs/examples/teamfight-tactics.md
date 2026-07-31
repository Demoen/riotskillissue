# Teamfight Tactics

```python
async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
    profile = await riot.tft.profile("Player#EUW")
    ranked = await riot.tft.ranked_entries("Player#EUW")
    history = await riot.tft.match_history("Player#EUW", count=5)
```

Use `riot.raw.tft` for the complete generated TFT API.
