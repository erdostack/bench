# trailgraph

The trail network behind the park's route planner. `junction` holds trailheads, forks and summits;
`segment` holds the trail between two junctions (`from_junction`, `to_junction`, length, surface). Routes are
recursive CTEs over `segment`.

Integrity: both ends of a segment are foreign keys to `junction` with `ON DELETE CASCADE`, so closing a
junction (`make close J=<id>`) removes its segments too, and the planner can never route over a segment that
leads to a junction that no longer exists.

Stack: Go 1.23, SQLite through github.com/mattn/go-sqlite3 v1.14.17, database file `data/trails.db`.

    make load                 # rebuild data/trails.db from db/schema.sql and data/*.csv
    make q F=sql/loop_from.sql
    make close J=J-0412       # close a junction for the season
