# Replay downloads

Download a League of Legends replay by player name through your running League
Client, or use Riot Sign On to download replays returned by the public API.
Both workflows are included in the base package.

To choose one of another player's recent matches, open League, sign in, and run:

```bash
riotskillissue-cli replays download --player "GameName#TagLine"
```

Use the full Riot ID, including the tag. The command shows recent matches and
asks which replay to download. This mode needs neither a Riot API key nor an
RSO token.

| Mode | Requirements | Replay source |
| --- | --- | --- |
| `--player "GameName#TagLine"` | Logged-in League Client on the same Windows or macOS machine | The named player's matches accessible to that client |
| Without `--player` | An access token from an approved RSO integration | Replays returned for the player identified by the token |

## Download by player name

Keep the League Client running while using these commands. The target player
and match must be accessible on the client's current region. `--route` is an
RSO-only option and cannot be combined with `--player`.

To inspect up to 20 recent matches:

```bash
riotskillissue-cli replays list --player "GameName#TagLine"
```

The table shows the selection number, match ID, queue, and patch. Recent matches
can include unavailable replays; the client checks the selected replay when you
request a download.

For interactive selection from a smaller list:

```bash
riotskillissue-cli replays download --player "GameName#TagLine" --count 5
```

Or select a one-based entry directly:

```bash
riotskillissue-cli replays download 1 --player "GameName#TagLine"
```

The League Client downloads the selected replay into its configured replay
folder. The CLI waits for completion and prints the resulting path. To keep a
copy somewhere else:

```bash
riotskillissue-cli replays download 1 --player "GameName#TagLine" --output ./replays/game.rofl
```

`--output` copies the completed replay to that file without changing the League
Client's settings. Missing parent directories are created. An existing output
file is preserved unless you pass `--overwrite`, and a failed copy leaves no
partially written destination.

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `--player` | Not set | Full `GameName#TagLine` Riot ID; enables the League Client workflow |
| `INDEX` | Interactive selection | One-based row to download; `download` only |
| `--count` | `20` | Recent matches to list, from `1` to `20`; player mode only |
| `--lockfile` | `RIOT_LCU_LOCKFILE`, then automatic discovery | Path to the running League Client's lockfile |
| `--timeout` | `120` | Seconds to wait for local download completion, from `1` to `600`; `download` only |
| `--output` | League Client's replay folder | Copy the completed replay to this file; `download` only |
| `--overwrite` | Off | Replace an existing `--output` file after a successful copy |

`--lockfile`, `--count`, and `--timeout` apply only when `--player` is set.

The list is fetched anew for each invocation. Its order may change between
`list` and `download 1`. Omit the index to choose from the exact list that the
download command will use. The number is a row selection, not a match ID.

!!! note "League Client API compatibility"
    This workflow uses the local
    [League Client API](https://developer.riotgames.com/docs/lol#league-client-api).
    Riot does not officially support it for third-party applications or
    guarantee compatibility between patches. Replay access remains subject to
    the current client's availability checks and server responses.

## Find your League client

The CLI checks these standard lockfile locations:

| Platform | Location |
| --- | --- |
| Windows | `C:/Riot Games/League of Legends/lockfile` |
| macOS | `/Applications/League of Legends.app/Contents/LoL/lockfile` |
| macOS, per-user installation | `~/Applications/League of Legends.app/Contents/LoL/lockfile` |

On Windows, the drive comes from `SYSTEMDRIVE`, normally `C:`.

For a custom installation, pass the exact path or set `RIOT_LCU_LOCKFILE`:

```powershell
riotskillissue-cli replays list --player "GameName#TagLine" --lockfile "D:/Riot Games/League of Legends/lockfile"
```

The lockfile is created by the running League Client and contains local
connection credentials. Use the file on your own machine; do not copy it from
another player or commit it to a repository. Run the command in the same Windows
or macOS environment as League, rather than a remote server, container, or WSL.

## Download limits

Riot's
[Patch 26.21 notes](https://www.leagueoflegends.com/en-ph/news/game-updates/league-of-legends-patch-26-21-notes/),
published on October 20, 2026, retain downloads of your own, friends', and other
players' replays with a limit of **10 downloads per hour**.

Player mode asks your League Client to download the replay and follows its
server-enforced limit, including downloads started through the client UI. The
CLI downloads one selected replay per invocation. It does not retry rejected
download requests or invent a local count of remaining downloads. If Riot
rejects a download, wait for the reported interval where available before trying
again.

That client announcement does not specify the public API's replay quota. The
RSO workflow below also respects rate-limit responses.

## What the endpoint supports

Without `--player`, RiotSkillIssue uses the public endpoint
[`match-v5.getReplayByAccessToken`](https://developer.riotgames.com/apis#match-v5/GET_getReplayByAccessToken):

```text
GET https://{route}.api.riotgames.com/lol/match/v5/matches/replays
Authorization: Bearer <RSO access token>
```

The response contains `total` and `matchFileURLs`. It lists replays for the
player identified by the access token. The endpoint has no Riot ID, PUUID,
match-ID, or pagination parameter. The CLI can download files from that list;
this RSO mode cannot look up another player's replay by name or match ID.
Use [player mode](#download-by-player-name) for a lookup through your local
League Client.

## Authentication

These requirements apply to the public API workflow, without `--player`.
Player mode uses the running League Client instead.

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

With an RSO token configured, list the authenticated player's public API replays:

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

For an interactive selection from the RSO replay list, run:

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

### League Client

Use `LeagueReplayClient` as an async context manager while League is running:

```python
import asyncio

from riotskillissue import LeagueReplayClient


async def main() -> None:
    async with LeagueReplayClient() as league:
        replays = await league.player_replays("GameName#TagLine", count=5)
        if replays:
            path = await league.download_replay(replays[0], timeout=120)
            print(path)


asyncio.run(main())
```

`player_replays()` returns `list[ClientReplay]` for the named player's recent
matches. Pass a `destination` to `download_replay()` to copy the completed replay
to another file; omit it to use the League Client's replay folder. The method
returns a `pathlib.Path` and accepts `overwrite=True` for replacing an explicit
destination. This client does not use `RiotClient`, an API key, or an RSO token.

### Public API with RSO

The async and sync Riot clients expose the same RSO workflow. Both examples read
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
| League Client not found | Open League and sign in. For a custom installation, pass `--lockfile` or set `RIOT_LCU_LOCKFILE`. |
| Player not found | Supply the full Riot ID, including `#TagLine`, and check that the player is accessible from the League Client's current region. |
| Match listed but replay unavailable | A match-history entry does not guarantee that Riot still offers its replay. The client may reject older or otherwise unavailable replays. |
| Local download timed out | Keep League open and check its download status. Increase `--timeout` if the transfer is slow; the timeout does not cancel the client's download. |
| Missing RSO access token | For commands without `--player`, set `RIOT_RSO_ACCESS_TOKEN`; an `RGAPI-...` API key cannot replace it. |
| RSO unauthorized or forbidden | Obtain a current token through your approved RSO integration and verify the player's authorization. |
| No RSO replays returned | Check the regional route and the replays available to the authenticated player. |
| Invalid selection | Select a number from the current list, starting at `1`, or omit it to choose interactively. |
| Destination already exists | Choose another `--output` path or use `--overwrite`. |
| Download expired or unavailable | Fetch a fresh list and retry the selection. A replay may no longer be available. |
| Rate limited | Wait for the reported retry interval where available; do not repeatedly request the same download. |
| RSO transfer interrupted | Retry once the connection is stable. Incomplete downloads are not kept as completed replay files. |

Downloaded `.rofl` files are game replays, not video exports. Downloading a file
does not launch League or convert it to another format.
