# Roast: hublane model

Foreign keys in a graph database. Somewhere a relational DBA smiles.

## Findings

### 1. Parcel.depot_code (high)

**Problem.** Denormalised foreign key held as a property alongside the canonical AT relationship. Dual sources of truth are an anti-pattern: they are prone to update anomalies and could drift apart over time.

**Fix.** Drop depot_code and the parcel_depot_status index; rewrite depot_backlog to MATCH (d:Depot {code: $depot})<-[:AT]-(p:Parcel) and filter on status.

### 2. depot_backlog (medium)

**Problem.** Label scan semantics on Parcel with a composite predicate.

**Fix.** Anchor on Depot instead.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
