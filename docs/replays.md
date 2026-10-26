# Replay downloads

List the League of Legends replays available to an authenticated player, choose
one, and save its `.rofl` file from the terminal. The commands are included in
the base package.

!!! important "An RSO access token is required"
    Replay discovery uses **Riot Sign On (RSO)**. A normal `RGAPI-...` developer
    API key is not sufficient. You need an access token issued after the player
    authorizes an approved RSO integration. See [authentication](#authentication)
    before trying the commands.

## What the endpoint supports

RiotSkillIssue uses
[`match-v5.getReplayByAccessToken`](https://developer.riotgames.com/apis#match-v5/GET_getReplayByAccessToken):

```text
GET https://{route}.api.riotgames.com/lol/match/v5/matches/replays
Authorization: Bearer <RSO access token>
```

The response contains `total` and `matchFileURLs`. It lists replays for the
player identified by the access token. The endpoint has no Riot ID, PUUID,
match-ID, or pagination parameter. The CLI can download files from that list;
it cannot look up an arbitrary other player's replay by name or match ID.

The public API and the game client have different interfaces. Riot's
[Patch 26.21 notes](https://www.leagueoflegends.com/en-ph/news/game-updates/league-of-legends-patch-26-21-notes/),
published on October 20, 2026, say the client still supports downloads of your
own, friends', and other players' replays, with a limit of 10 downloads per hour.
That announcement does not specify the public API's download quota. Respect
the limits and availability returned by the service you are using.

## Authentication

[Riot's RSO integration guide](https://developer.riotgames.com/docs/lol#rso-integration)
requires an approved production-key application and RSO onboarding. The player
then signs in through Riot's authorization flow. The replay operation requires
the `openid` scope.

RiotSkillIssue provides [RSO helpers](rso.md) for applications that already have
that integration. The CLI accepts an existing access token; it does not register
an application, run a browser login, or extract tokens from the League client.

Set the token in the terminal where you will run the replay commands:

=== "macOS / Linux"

    ```bash
    export RIOT_RSO_ACCESS_TOKEN="your-rso-access-token"
    ```

=== "Windows PowerShell"

    ```powershell
    $env:RIOT_RSO_ACCESS_TOKEN = "your-rso-access-token"
    ```

Both commands also accept `--access-token`. Using the environment variable keeps
the token out of the replay command's arguments. Treat access tokens and signed
download URLs as credentials. No `RIOT_API_KEY` is needed for these commands.

## List available replays

```bash
riotskillissue-cli replays list --route europe
```

The table shows a one-based selection number and a suggested filename. The CLI
does not print the signed download URLs. Choose the regional route that holds
the player's replays: `americas`, `asia`, `europe`, or `sea`. The default is
`europe`; platform routes such as `euw1` are not accepted here.

Riot returns URLs without separate match metadata. A filename is inferred when
the URL contains a usable name; otherwise the command supplies a fallback.
Do not assume every row includes a match ID, date, champion, or game mode.

## Download a replay

For an interactive selection, run:

```bash
riotskillissue-cli replays download --route europe
```

The command fetches the list and asks which entry to download. It downloads
from that same list, so the selected number refers to the row you just saw.

To select a number directly and choose a destination:

```bash
riotskillissue-cli replays download 1 --route europe --output ./replays/my-game.rofl
```

Each command fetches the current list. Its order and contents may change between
a separate `list` call and `download 1`; use interactive selection when you want
to inspect the exact list being used. Numbers start at **1** and are not match
IDs.

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `INDEX` | Interactive selection | One-based entry in the current list; `download` only |
| `--route` | `europe` | `americas`, `asia`, `europe`, or `sea` |
| `--access-token` | `RIOT_RSO_ACCESS_TOKEN` | RSO access token |
| `--output` | Suggested filename in the current directory | Destination file; `download` only |
| `--overwrite` | Off | Replace an existing destination after a successful download |

Files are streamed to disk, and missing parent directories are created. The
destination is published only after the transfer completes; a failed transfer
cleans up its temporary file and preserves any existing destination. To replace
a file deliberately:

```bash
riotskillissue-cli replays download 1 --output ./replays/my-game.rofl --overwrite
```

The command downloads one file per invocation and does not retry file downloads
automatically. If the server limits requests, wait before trying again. Run
`riotskillissue-cli replays download --help` for the installed version's options.

## Use from Python

The async and sync clients expose the same workflow. Both examples read
`RIOT_RSO_ACCESS_TOKEN` from the environment.

=== "Async"

    ```python
    import asyncio

    from riotskillissue import RegionalRoute, RiotClient


    async def main() -> None:
        async with RiotClient() as riot:
            replays = await riot.lol.replays(route=RegionalRoute.EUROPE)
            for replay in replays:
                print(replay.index, replay.filename)
            if replays:
                path = await riot.lol.download_replay(
                    replays[0], "replays/my-game.rofl"
                )
                print(path)


    asyncio.run(main())
    ```

=== "Sync"

    ```python
    from riotskillissue import RegionalRoute, SyncRiotClient

    with SyncRiotClient() as riot:
        replays = riot.lol.replays(route=RegionalRoute.EUROPE)
        if replays:
            path = riot.lol.download_replay(replays[0], "replays/my-game.rofl")
            print(path)
    ```

`replays()` returns `list[ReplayFile]`. Each entry has `index`, `filename`, and
`url`; the URL is omitted from the object's representation. `download_replay()`
returns a `pathlib.Path` and accepts `overwrite=True` for explicit replacement.
Keep returned entries only as long as needed to download them, since signed
URLs may expire.

When embedding the client in an application, keep HTTP request logging disabled
for replay downloads: `httpx` INFO logs and `httpcore` debug logs can include
signed URLs. The CLI does not enable that logging.

For applications that need the unmodified response, the generated method remains
available:

```python
replay_data = await riot.raw.lol.match.get_replay_by_access_token(
    route=RegionalRoute.EUROPE,
)
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Missing access token | Set `RIOT_RSO_ACCESS_TOKEN`; an `RGAPI-...` API key cannot replace it. |
| Unauthorized or forbidden | Obtain a current token through your approved RSO integration and verify the player's authorization. |
| No replays returned | Check the regional route and the replays available to the authenticated player. The CLI cannot request files absent from the list. |
| Invalid selection | Select a number from the current list, starting at `1`, or omit it to choose interactively. |
| Destination already exists | Choose another `--output` path or use `--overwrite`. |
| Download expired or unavailable | Fetch a fresh list and retry the selection. A replay may no longer be available. |
| Rate limited | Wait for the reported retry interval where available; do not repeatedly request the same download. |
| Transfer interrupted | Retry once the connection is stable. Incomplete downloads are not kept as completed replay files. |

Downloaded `.rofl` files are game replays, not video exports. Downloading a file
does not launch League or convert it to another format.
