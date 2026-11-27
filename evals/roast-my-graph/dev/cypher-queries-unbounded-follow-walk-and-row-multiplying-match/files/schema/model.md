# Model

| Relationship | From | To | Properties |
|---|---|---|---|
| `FOLLOWS` | `Listener` | `Listener` | `since` |
| `PLAYED` | `Listener` | `Track` | `at` |
| `BY` | `Track` | `Artist` | |
| `IN_GENRE` | `Track` | `Genre` | |

`(a)-[:FOLLOWS]->(b)` means a follows b, so b's followers are the listeners pointing at b.
