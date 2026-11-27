# Model

`nodes.kind`: `object` or `location`. `nodes.code` is unique: accession numbers for objects
(`1974.33.2`), location codes for locations (`G7`, `STORE-B`, `OFF-1`).

`edges` holds one `located_in` edge per object: `src` the object, `dst` its location, `since` the date it
arrived there (TEXT, YYYY-MM-DD).

## The OFF-1 move

Objects moved to the offsite store OFF-1 during 2025-26 were recorded by an older version of the movement
app, which set `nodes.location_code = 'OFF-1'` and `nodes.moved_on`, and deleted the object's old
`located_in` edge without adding the new one. So those objects have no `located_in` edge at all until it
is backfilled: one edge to OFF-1 per object, with `since` = `moved_on`.
