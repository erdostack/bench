# Model

`nodes.kind` is `show`, `presenter`, `track` or `episode`. Only episodes have `aired_on`.

| edge kind | src | dst | per episode |
|---|---|---|---|
| `episode_of` | episode | show | 1 |
| `hosted_by` | episode | presenter | 1 or 2 |
| `played` | episode | track | up to 20 |
| `repeat_of` | the repeat episode | the episode it repeats | out: 0 or 1; in: up to 2 (added in 2024) |

So an episode has at most 26 edges, counting both ends. Since 2024 a repeat broadcast is its own episode
with a `repeat_of` edge to the original, so an old episode can be the `dst` of an edge from a newer one.
