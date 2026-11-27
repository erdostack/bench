# heatnet

Pipe graph of the district heating network: plants, junctions and buildings are nodes, pipes are edges.
Operations asks "which buildings lose heat if this valve closes", so most queries are recursive walks
downstream from a junction.

## Storage

One SQLite file, `data/heat.db` (built by `make load` from `data/csv/`; not committed). The Go code talks to
it through github.com/mattn/go-sqlite3, which compiles SQLite into the binary with cgo, so there is no server
to run. The engine is SQLite 3.45.1, the amalgamation that ships with go-sqlite3 v1.14.22.

## Running a query

    make q F=queries/downstream_buildings.sql ARGS=J-104

`heatq` opens the file read-only and prints rows as tab-separated text. Writes go through `make load` only,
which the network data team runs after each survey.
