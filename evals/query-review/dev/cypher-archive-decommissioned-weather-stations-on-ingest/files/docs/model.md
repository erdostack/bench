# Model (Neo4j 5.26)

    (:Station {code, name, status, commissionedOn, decommissionedOn})-[:HAS_SENSOR]->(:Sensor {serial, kind})
    (:Station)-[:IN_REGION]->(:Region {code})

Types: `commissionedOn` and `decommissionedOn` are DATE values (the asset system writes them with
`date()`); `code`, `name` and `status` are strings.

`Station.status` is one of:

| status | meaning |
|---|---|
| `active` | reporting |
| `suspended` | temporarily offline (maintenance, flood damage, a lost lease); expected back |
| `decommissioned` | closed for good on `decommissionedOn` |

Archiving: a decommissioned station is kept as `Station` until the end of the calendar year after it
closed, so the QC jobs can still reach its late data. After that it is archived: it carries the label
`ArchivedStation` instead of `Station`, keeps its properties and relationships, and drops off the map and
the API. Only decommissioned stations are ever archived.

Counts (2026-11-20): 4,108 stations: 3,402 active, 211 suspended, 495 decommissioned (412 of them before 2025).
