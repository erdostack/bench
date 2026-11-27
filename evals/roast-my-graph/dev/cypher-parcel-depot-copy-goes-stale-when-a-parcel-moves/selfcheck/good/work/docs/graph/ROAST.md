# Roast: hublane model

The README promises the copy and the relationship never disagree. They disagree for seven parcels in ten.

## Findings

### 1. move_parcel (critical)

**Problem.** The parcel's depot is written down twice: the AT relationship and the depot_code property. This statement moves the relationship to the next depot and does not change the property, so from the first move onwards the property names the depot the parcel left. depot_backlog, the screen every dispatcher works from, filters on that property: moved parcels show up in the wrong depot's backlog and are invisible where they are waiting. parcel_trace and depot_load follow the relationship and will contradict the screen.

**Fix.** Add the property to the same statement: SET p.status = 'waiting', p.depot_code = next.code. Then repair what is already wrong once: MATCH (p:Parcel)-[:AT]->(d:Depot) WHERE p.depot_code <> d.code SET p.depot_code = d.code (in batches). A nightly count of that same mismatch should stay at zero.

### 2. mark_delivered (low)

**Problem.** A delivered parcel keeps its AT relationship and its depot_code. Harmless for depot_backlog because of the status filter, but depot nodes collect relationships for ever.

**Fix.** Decide whether delivered parcels should keep AT; if not, delete it here.

### 3. depot_load (low)

**Problem.** Counts by walking every AT relationship of the depot, delivered parcels included. Nightly, so fine for now.

**Fix.** Could read the same index as depot_backlog once depot_code can be trusted.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
