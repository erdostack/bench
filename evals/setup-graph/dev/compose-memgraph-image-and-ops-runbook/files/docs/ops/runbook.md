# Runbook

## Version

Memgraph 2.21.0 Community. Snapshots are written on exit and every 300 seconds to the `mg-data`
volume.

## Restart after a crash

1. `docker compose restart memgraph`
2. Wait for the log line saying the snapshot was recovered.
3. Run `queries/sanity_counts.cypher` and compare with yesterday's numbers in the dashboard.
