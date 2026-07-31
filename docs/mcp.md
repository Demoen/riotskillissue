# Local MCP server

Install the optional dependency:

```bash
pip install "riotskillissue[mcp]"
```

Configure your MCP client to launch:

```json
{
  "command": "riotskillissue-mcp",
  "env": {
    "RIOT_API_KEY": "RGAPI-...",
    "RIOT_DEFAULT_ROUTE": "euw1"
  }
}
```

The 1.0 server supports local stdio only. It writes protocol messages to stdout
and diagnostics to stderr.

## Tools

High-level tools cover profiles, match history, ranked entries, leaderboards,
live games, mastery, challenges, service status, and game content.

The raw gateway uses five compact tools:

- `riot_find_operations`
- `riot_describe_operation`
- `riot_call_read_operation`
- `riot_call_write_operation` when writes are enabled
- `riot_read_result`

RSO and OAuth operations are not discoverable. Keys and tokens are read from the
server environment and never appear in tool schemas.

## Large results

Results up to 32 KiB are returned inline. Larger values are retained in memory
for ten minutes and returned as an opaque handle with a structural outline.
`riot_read_result` supports RFC 6901 JSON Pointers and paginated list or mapping
slices. Retained results are never written to disk.

## Writes

Writes are hidden by default. Set `RIOT_MCP_ALLOW_WRITES=true` to register the
write tool. Each call still requires resolver-based human confirmation and
fails closed if confirmation is declined, cancelled, or unsupported.
