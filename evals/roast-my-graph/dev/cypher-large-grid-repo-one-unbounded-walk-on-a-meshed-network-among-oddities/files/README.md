# gridmap

The network model of an electricity distribution company: what is connected to what, where it is, and who
is supplied from it. Neo4j 5.

| Path | What |
|---|---|
| `docs/model.md` | labels, relationships and keys |
| `cypher/schema.cypher` | constraints and indexes |
| `cypher/ingest/` | statements run by the nightly sync from the asset register and the billing system |
| `cypher/queries/assets.cypher` | asset screens in the field app |
| `cypher/queries/outage.cypher` | the control room's outage planner |
| `cypher/queries/reports.cypher` | scheduled reports |

Every statement starts with a `// name:` line; that is the name the applications call it by.

## Numbers

| Thing | Count |
|---|---|
| `Zone` | 2,900, in a tree exactly four levels deep (region, district, depot area, block) |
| `Asset` | 410,000 (2,100 substations, 190,000 transformers, the rest switches and joints) |
| `CONNECTS` | 640,000 |
| `Meter` | 3.4 million |
| `Customer` | 2.9 million |
| `WorkOrder` | 1.1 million, about 9,000 open |

The cable network is meshed: most transformers can be reached from two or three substations, and it is run as
separate trees only by leaving some switches open. Every cable is in the graph whether its switch is open or
closed (`CONNECTS.normally_open`).

## Who runs what

- Field app (`assets.cypher`): a few hundred engineers, interactive.
- Outage planner (`outage.cypher`): control room operators, interactive, during planned work and during
  faults. Screens are expected to answer within two seconds.
- Reports (`reports.cypher`): scheduled overnight, no time limit worth mentioning.
