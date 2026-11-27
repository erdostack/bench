# Model

A `networkx.DiGraph`. Every node has a `kind`; every edge has a `kind`.

| node kind | id | attributes |
|---|---|---|
| `person` | `P1042` | `firstName`, `lastName`, `creationDate` (ISO text, UTC) |
| `city` | `city:ellerby` | `name` |
| `tag` | `tag:chess` | `name` |

| edge kind | from | to | attributes |
|---|---|---|---|
| `knows` | person | person | `creationDate` |
| `isLocatedIn` | person | city | |
| `hasInterest` | person | tag | |

A friendship is one `knows` edge, stored once per pair, from the person who sent the friend request to the
one who accepted it. It means the same thing whichever way it points: the suggestion code reads it in both
directions.
