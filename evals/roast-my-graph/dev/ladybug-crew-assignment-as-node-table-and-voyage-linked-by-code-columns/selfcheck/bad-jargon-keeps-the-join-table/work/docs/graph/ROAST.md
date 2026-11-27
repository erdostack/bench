# Roast: fleetlog

Tables in a trench coat, foreign keys as properties: the classics.

## Findings

### 1. CrewAssignment (high)

**Problem.** Tables in a trench coat: this is a relational join table ported one-to-one into the graph, and its sailor_id and vessel_imo columns are not indexed.

**Fix.** Keep the node table but add secondary indexes on CrewAssignment.sailor_id and CrewAssignment.vessel_imo so the join columns are searchable.

### 2. Voyage.origin_port_code (medium)

**Problem.** Foreign keys as properties anti-pattern: the code columns are STRING, which is slow to compare.

**Fix.** Change origin_port_code, dest_port_code and vessel_imo to INT64 surrogate keys so the comparisons in the queries are cheaper.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
