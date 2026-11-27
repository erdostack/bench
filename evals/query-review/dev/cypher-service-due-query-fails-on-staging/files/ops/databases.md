# Databases

| target | server | database `bikes` |
|---|---|---|
| prod | self-managed cluster, 3 servers, Neo4j 2026.10.2 | created 2024-09 on Neo4j 5.23; upgraded in place since (5.26 -> 2025.04 -> 2026.10.2) |
| staging | one server, Neo4j 2026.10.2 | restored from a prod backup on 2026-10-30 |
| local | your laptop, `docker-compose.yml` | created fresh by `docker compose up` |

Upgrades are done with the rolling procedure in the upgrade guide; nothing else is changed on the
databases during an upgrade. `ops/neo4j.conf` is the config of the prod and staging servers.
