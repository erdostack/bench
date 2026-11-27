# linkup-core

Core services of linkup, the professional social network: members, friendships, posts. Production data is in
PostgreSQL 16 (`db/schema.sql`), one primary and two read replicas; services read from the replicas.

- `services/profile/`: the profile page backend (Python).
- `docs/incidents/`: write-ups of past incidents.
