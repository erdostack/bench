# ferrylink

Ferry crossings between harbours (generated timetable), stored as two SQLite tables in data/ferry.db, with
recursive CTEs for "reachable within N crossings" questions.

- Scala 3, sbt; SQLite through sqlite-jdbc 3.45.3.0
- Run a query: `make q F=sql/reachable.sql`
- `make check` lists crossings whose destination port is missing. It prints nothing, so the crossing data is
  clean and the CTEs can assume both ends exist.
- Schema: db/schema.sql
