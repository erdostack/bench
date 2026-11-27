# Review

Add range indexes on upstream_ids for Meter and Transformer and the outage queries will use index
seeks.

## Meter.upstream_ids (high)

Unindexed predicate: label scan on Meter for a list-membership test (the denormalised adjacency list anti-pattern), causing NodeByLabelScan + Filter.

Fix: CREATE INDEX meter_upstream FOR (m:Meter) ON (m.upstream_ids); same for Transformer.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
