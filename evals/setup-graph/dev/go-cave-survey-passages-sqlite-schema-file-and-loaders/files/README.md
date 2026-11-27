# cavesurvey

The club's cave survey as a graph: survey stations are nodes, measured passages (shots) between them are
edges with length, bearing and inclination. We use it for "how do I get from the entrance to station X"
and for checking which parts of the system hang off a single squeeze.

Storage is one SQLite file, `data/caves.db`, used from Go through github.com/mattn/go-sqlite3 v1.14.17
(cgo). See docs/DATA.md for the tables and what the database guarantees.

    make q F=queries/route_from_entrance.sql ARGS=ST-214

`make init`, `make load` and `make merge` change the database; the survey officer runs them after each trip.
