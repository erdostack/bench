# driveshare

File sharing backend. Folders form a tree per owner; a share grants someone a role on a folder.

- Python 3.12, FastAPI, psycopg 3, Postgres 16 (one primary, two replicas).
- `db/schema.sql` is the current schema.
- `drive/shares.py` creates and revokes shares.
