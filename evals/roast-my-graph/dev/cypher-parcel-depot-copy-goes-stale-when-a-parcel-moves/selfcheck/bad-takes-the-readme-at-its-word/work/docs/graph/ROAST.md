# Roast: hublane model

A clean little model with one deliberate shortcut.

## Findings

### 1. Parcel.depot_code (low)

**Problem.** Deliberate denormalisation of the AT relationship for the parcel_depot_status index. Documented, with a clear read pattern, and maintained by the write statements.

**Fix.** Keep it. Consider a periodic consistency check.

### 2. depot_backlog (low)

**Problem.** LIMIT 200 with no paging.

**Fix.** Add keyset paging if depots ever hold more than 200 waiting parcels.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
