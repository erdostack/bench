# harness-viewer

Internal web tool for the e-bike wiring harnesses: browse a harness variant, open a connector, trace a
circuit from a pin to everything it reaches through wires, splices and connector pins. Data comes from
the harness design export into Postgres (`db/schema.sql`), one schema per engineering release.

- Python 3.12, `pip install -r requirements.txt`.
- Deployed as two containers behind the intranet proxy (`deploy/viewer.yaml`).
