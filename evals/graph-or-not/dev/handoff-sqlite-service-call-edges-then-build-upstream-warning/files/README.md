# deploytool

The deploy CLI. Its SQLite database (`var/deploy.db`, schema in `db/schema.sql`) holds the service list, deploy
history and the call graph from tracing, loaded nightly.

- `deploytool/impact.py`: who a deploy might affect.
- `deploytool/cli.py`: entry point.
