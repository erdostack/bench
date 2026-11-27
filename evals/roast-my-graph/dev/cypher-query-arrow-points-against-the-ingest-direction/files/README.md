# opsmap

What runs where, and who to wake up. Neo4j 5.

| Path | What |
|---|---|
| `docs/model.md` | the model in one table |
| `cypher/constraints.cypher` | constraints and indexes |
| `cypher/ingest.cypher` | how the inventory sync writes the graph (every 10 minutes) |
| `cypher/ops_queries.cypher` | queries used by the on-call tooling, each with a `// name:` line |

Numbers: 410,000 hosts (VMs included), 6,200 services, 180 teams, 9,500 racks.

Who calls what:

- `host_by_serial`: the provisioning agent on every host, at boot and with each heartbeat. About 600 calls a second.
- `services_on_host`, `owners_to_page`: the incident bot, when a host alert fires.
- `upstream_of`, `rack_inventory`, `tier_one_services`: dashboards, a few times a minute.
