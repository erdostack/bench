# registry-graph

Package dependency graph of the internal package registry. `var/registry.db` is a copy of the
service database; the schema is `db/migrations/` applied in order.

Everything that reads this database goes through the files in `queries/`:

| File | Used by | When |
|---|---|---|
| `queries/package_page.sql` | registry web UI | every page view |
| `queries/dependencies.sql` | registry web UI, resolver | every page view, every install |
| `queries/weekly_dependents_report.sql` | `report-dependents` job | Mondays 06:00, once per top-500 package |

The importer (another repository) inserts new packages and dependency edges every night.

    ./rq "SELECT count(*) FROM packages"
    ./rq -f queries/dependencies.sql -p pkg=1042
    python3 tools/index_usage.py
