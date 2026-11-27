# Migrations

Files are `migrations/V<NNN>__<what>.cypher`, applied once each, in order, by `tools/migrate.py`
when a release deploys. Never edit an applied file; add a new one.

- A file runs inside one managed transaction, so a failing migration leaves nothing behind. See the
  runner's docstring for files that cannot run that way.
- Keep any one transaction under about 200,000 changed properties; the production heap is 8 GB.
- No plugins are installed on any of our servers (no APOC, no GDS).
