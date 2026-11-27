# county-bus

Timetables and transfer planning for the county bus network.

- `web/` is the timetable site (plain JDBC to the timetable database, no graph).
- `graph/` holds the transfer graph: an embedded Kuzu 0.10.0 database (no server) in `var/transfers.kz`,
  built from `data/` by `bin/load` and queried with `bin/kq`:

      bin/kq graph/queries/reachable_in_two_changes.cypher stop=S01

The node and relationship tables are in `graph/src/main/resources/schema.cypher`.
