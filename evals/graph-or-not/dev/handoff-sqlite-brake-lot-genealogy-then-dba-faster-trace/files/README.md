# tracelink

Lot genealogy for the brake components business: which lots went into which, from raw material to shipped
units, across the plants.

- Python 3.12, Postgres 16 (partitioned by plant). Tests use a SQLite file built from `db/schema.sql`.
- Links arrive from each plant's MES through the `ingest/` consumers.
- `trace/recall.py` answers the quality team's forward (containment) and backward (root cause) questions.
