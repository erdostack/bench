# fleetgraph

Sensors and gateways of the cold-chain fleet, and the firmware rollout rings. `ring_members` links a
device to its ring; `rings.member_count` is kept next to it for the rollout tool. `var/fleet.db` is a
copy of live; schema in `db/schema.sql`.

- `jobs/`: nightly jobs, `run(conn)`; `python -m jobs <name> [db]`. Rules in `docs/jobs.md`.
- `logs/`: job logs from the ops box.
