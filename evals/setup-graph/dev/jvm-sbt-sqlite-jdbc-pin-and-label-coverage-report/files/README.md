# propagation

Records which garden specimens were propagated from which (cuttings, divisions, grafts), so a curator
can trace a plant back to the accession it came from, and checks that every specimen bed has a label.

## Store

One SQLite file, `data/garden.db`, read through the xerial sqlite-jdbc driver 3.46.1.0. The driver
bundles SQLite itself, and its version number is the SQLite version it carries (3.46.1.0 is SQLite
3.46.1). The propagation tree is `specimen.parent_id`; lineage queries are recursive CTEs.

    make q F=sql/ancestry.sql ARGS=SP-0219     # one query file
    make report                                # sql/reports/*.sql

Schema: `db/schema.sql`.
