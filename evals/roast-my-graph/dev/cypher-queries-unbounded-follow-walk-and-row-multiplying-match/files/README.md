# tunefeed graph

The social layer of the player: who follows whom and what they played. Neo4j 5, one primary and two read replicas.

| What | How many |
|---|---|
| `Listener` | 38 million |
| `FOLLOWS` | 1.9 billion (median 22 per listener) |
| `Track` | 71 million |
| `PLAYED` | about 6 billion, 90 days kept |
| `Artist` | 4.2 million |
| `Genre` | 610 |

`queries/feed.cypher` holds the queries behind the profile and home screens. Each starts with a `// name:` line,
which is the name the API layer calls it by. The budget for every one of them is 150 ms at p95.

`schema/` has the constraints and a short description of the model.
