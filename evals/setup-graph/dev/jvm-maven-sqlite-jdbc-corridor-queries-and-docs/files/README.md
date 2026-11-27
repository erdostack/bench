# corridors

Habitat patches and the wildlife corridors between them, from the county's camera-trap surveys
(generated data in this repo). The graph is two tables in a SQLite file, `data/corridors.db`:
`patch` and `corridor` (one row per direction an animal was seen moving).

## Running a query

    bin/sql queries/reachable_patches.sql P-07

`bin/sql` runs `org.example.corridors.Sql` through Maven. It opens the database read-only.

## Dependencies

Java 17 and Maven. SQLite comes from the sqlite-jdbc driver, which bundles its own SQLite: driver
version 3.X.Y.Z ships SQLite 3.X.Y. There is no separate SQLite to install.

See `docs/queries.md` before writing new query files.
