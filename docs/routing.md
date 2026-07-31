# Routing

Riot uses three distinct route families:

- `PlatformRoute` for game shards such as `EUW1` and `NA1`.
- `RegionalRoute` for clusters such as `EUROPE` and `AMERICAS`.
- `ValorantRoute` for VALORANT clusters such as `EU` and `NA`.

```python
from riotskillissue import PlatformRoute, RiotClient

riot = RiotClient(default_route=PlatformRoute.EUW1)
```

The client derives another route family only when the mapping is unambiguous.
For example, `EUW1` maps to `EUROPE` and `EU`. Calls that cannot be inferred
raise a typed route-resolution error and require an explicit `route=`.

Raw endpoints validate both the route family and the operation's allowed route
set before making a request.
