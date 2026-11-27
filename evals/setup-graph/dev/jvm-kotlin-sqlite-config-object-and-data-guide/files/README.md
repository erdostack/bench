# sortnet

The trunk network between parcel sorting centres: which centre sends a trailer to which, and the
cheapest chain of legs from any depot to any delivery office.

## Store

One SQLite file, `data/routes.db`, through sqlite-jdbc 3.47.0.0 (see `gradle/libs.versions.toml`).
Centres are rows in `centre`, legs are rows in `leg`; routes are recursive CTEs in `sql/`.

    bin/sql sql/cheapest_chain.sql DEP-N OFF-17

`bin/retire <code>` removes a centre that has closed. How the data is kept consistent is described
in `docs/DATA.md`.
