# stopgraph

Answers "where can I get to from here, and how fast" over the regional stop network. The network is a
graph kept in one SQLite file, `data/stops.db`: stops are rows in `stop`, direct rides between two stops
are rows in `link`, and reachability is a recursive CTE over `link`.

## Requirements

- Go 1.23
- Docker (queries run inside the image)
- SQLite: the image links against the system library, 3.46.1, compiled in the Dockerfile

## Running a query

    make image                          # once, or after a dependency change
    make q Q=queries/reachable_within.sql ARGS="S-0007 25"

`stopq` prints tab-separated rows with a header line. It opens the database read-only (`mode=ro`).

## Layout

- `cmd/stopq/` the query runner
- `sql/schema.sql` the two tables and their index
- `queries/` saved queries; positional parameters are `?1`, `?2`, ...
- `data/stops.db` the network, rebuilt nightly by the timetable job in another repo; do not edit it here
