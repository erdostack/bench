# linkfinder

Tools for the procurement integrity unit: who is connected to whom across the company register, officer
appointments, shareholdings, shared addresses and awarded contracts (all from public registers). The data is
loaded into one SQLite database (`var/registry.db`, schema in `db/schema.sql`) by the weekly import, which
lives in the data team's repo.

- `investigate/queries.py`: the canned questions analysts run.
- `tools/make_sample.py`: builds `var/sample.db`, a small synthetic database for tests and laptops.

Python 3.11+, no third-party packages.
