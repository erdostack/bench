# Schema snapshot

Taken with `CALL db.schema.visualization()` and `SHOW CONSTRAINTS` against the local container.

## Node labels

| Label | Properties |
|---|---|
| Tree | tag (string, unique), planted (integer) |
| Variety | name (string, unique) |
| Rootstock | name (string) |
| Row | name (string, unique) |

## Relationship types

| Type | From | To |
|---|---|---|
| OF_VARIETY | Tree | Variety |
| SCION_FROM | Tree | Tree |
| ON_ROOTSTOCK | Tree | Rootstock |
| IN_ROW | Tree | Row |
| ADJACENT_TO | Row | Row |
| POLLINATED_BY | Variety | Variety |
