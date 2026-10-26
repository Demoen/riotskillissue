# Riot Sign On

Riot Sign On operations use OAuth bearer tokens instead of `X-Riot-Token`.
Operation security metadata selects the correct authentication scheme.

RSO requires a production-key application approved by Riot and a completed RSO
integration. Players authorize access through Riot's sign-in flow. See
[Riot's onboarding instructions](https://developer.riotgames.com/docs/lol#rso-integration).
A developer API key alone does not grant access to RSO operations.

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

For an existing access token, set `RIOT_RSO_ACCESS_TOKEN` before constructing a
client, or pass a `StaticRsoTokenProvider`:

```python
import os

from riotskillissue import RegionalRoute, RiotClient, StaticRsoTokenProvider

provider = StaticRsoTokenProvider(os.environ["RIOT_RSO_ACCESS_TOKEN"])

async with RiotClient(rso_token_provider=provider) as riot:
    replays = await riot.lol.replays(route=RegionalRoute.EUROPE)
```

A static token is not refreshed automatically. Use the refreshing provider
above for an application that holds a refresh token.

Replay discovery is also available through the [replay CLI](replays.md).
RSO operations remain available in Python and are deliberately excluded from
the MCP server.
