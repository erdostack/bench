# waymarks

Waypoints and walking legs of a generated network of pilgrim ways, kept in PostgreSQL as two tables,
`waypoint` and `leg`. Route options and loops are recursive queries in sql/.

- Database: PostgreSQL 16. The nightly Jenkins job starts it, loads data/ and runs every query in sql/.
  Locally, point the usual PG* variables at any PostgreSQL.
- Java 21, Gradle. `./gradlew load` loads data/; `./gradlew sql -Pfile=sql/route_options.sql` runs one query.
- Schema: sql/schema.sql. Query conventions: docs/queries.md.
