# Model

`nodes.kind` is `player` or `event`.

| edge kind | src | dst | other columns |
|---|---|---|---|
| `entered` | player | event | |
| `paired` | player with white | player with black | `event` (event node id), `round`, `result` |

Test events made by the pairing engine's load test have codes starting `TST-`; the load test plays its
games between ordinary sandbox players.
