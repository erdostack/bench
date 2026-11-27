# depgraph

Queries over the internal package registry's dependency graph, used by the release dashboard to show
who is affected when a package ships a breaking change.

`var/registry.db` is a SQLite export of the registry: about 15,000 packages and 51,000 declared
dependencies (`schema.sql`). A dependency of any kind (runtime, dev or peer) counts as "depends on".

    python -m unittest discover -s tests          # unit tests, tiny in-memory graph
    scripts/sq "SELECT count(*) FROM depends_on"   # poke at the real export
    scripts/sq -f sql/largest_packages.sql -p min_dependents=500

`scripts/sq` reads `sq.toml`, logs each statement to `.sq_history`, and interrupts statements that
run past `statement_timeout_s`.

Functions in `depgraph/impact.py` take an open `sqlite3` connection as their first argument; the
dashboard owns the connection.
