# wayfind

Footpath graph behind the campus wayfinding kiosks. Doors, junctions and lift landings are rows in
`junction`; every walkable piece of path is a row in `segment` (one row per direction). Routes are recursive
CTEs over those two tables.

Engine: SQLite 3.45 (WebAssembly build), running inside Node; there is no database server. The kiosk loads
`data/campus.sqlite` into memory at start-up and never writes to it.

    pnpm install
    pnpm sql queries/step_free_reach.sql       # run any .sql file, print the rows
    pnpm route D-LIB-1 D-SCI-3                  # shortest walk between two doors

`data/campus.sqlite` is rebuilt by the estates team's export (`pnpm seed` rebuilds it from `sql/`).
