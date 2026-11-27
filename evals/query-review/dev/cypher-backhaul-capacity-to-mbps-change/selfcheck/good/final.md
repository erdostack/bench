Added `db/changes/0088_backhaul_capacity_mbps.cypher`. It converts every BACKHAUL that still has
`capacityKbps`: `capacityMbps = capacityKbps / 1000.0` (the `.0` matters: integer / integer truncates in Cypher,
so 2,500 would become 2), then removes `capacityKbps`, 10,000 links per transaction.
The `WHERE l.capacityKbps IS NOT NULL` is there because docs/changes.md says a failed release retries the file
from the top: without it, a retry would set capacityMbps to null on every link already converted (null / 1000.0
is null). To check before and after: `MATCH ()-[l:BACKHAUL]->() WHERE l.capacityKbps IS NOT NULL RETURN count(l)`
(410k before, 0 after), and EXPLAIN the file first. queries/hub_uplink_capacity.cypher still reads capacityKbps;
it needs to switch in the same release, as the ticket says.
