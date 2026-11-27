# boxroute

Container flows between ports for the network-planning team.

- `box_legs`: one row per container carried from one port to the next, by the day it was discharged.
- `lanes`: the port-to-port graph the planners and the rotation optimiser read: all-time box counts per
  (origin, dest). `box_legs` is only kept for 400 days, so `lanes` cannot be rebuilt from it.
- `db/schema.sql`; `var/boxroute.db` is a copy of live.
- `jobs/`: `run(conn, ...)`, `python -m jobs <name> [db]`. Rules in `docs/jobs.md`.
