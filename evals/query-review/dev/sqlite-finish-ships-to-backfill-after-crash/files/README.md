# dairylink

The milk cooperative's supply graph: member farms, the processing plants they ship to, and the hauliers
that collect. Built from the collection tickets the tankers print at every pickup.

- `db/schema.sql`; `var/dairylink.db` is a copy of live.
- `jobs/`: `python -m jobs <name>`; rules in `docs/jobs.md`.
- `logs/`: job logs.
- `docs/graph.md`: what the edges mean.
