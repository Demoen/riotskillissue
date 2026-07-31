# Riot Sign On

Riot Sign On operations use OAuth bearer tokens instead of `X-Riot-Token`.
Operation security metadata selects the correct authentication scheme.

`RsoClient` exchanges an authorization code and creates an automatically
refreshing provider that can be passed once to `RiotClient`. Endpoint methods do
not accept tokens.

```python
provider = await rso.exchange_code_for_provider(
    code,
    code_verifier=verifier,
)

async with RiotClient(
    default_route=PlatformRoute.EUW1,
    rso_token_provider=provider,
) as riot:
    match = await riot.raw.lol.rso_match.get_match(match_id="...")
```

RSO operations remain available in Python but are deliberately excluded from
the MCP server.
