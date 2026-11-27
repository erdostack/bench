# leasebook

Leases for a housing association, in Neo4j 5.

    graph/schema.cypher    constraints and indexes
    graph/load.cypher      nightly load from the property system's CSV export
    graph/queries.cypher   queries behind the staff portal; each has a `// name:` line
    data/sample/           the first rows of each export file, for reference

The loader reads each CSV with a plain CSV reader and sends the rows to the matching statement in
`load.cypher` as `$rows`, 1,000 at a time, exactly as they are in the file.

## Who calls what

- `expiring_leases`: the renewal desk, every morning, for one building and the coming three months. Tenants
  on that list get their renewal letter.
- `rent_roll_on`: finance, monthly: every lease in force on a given day.
- `tenant_history`, `unit_card`: the portal's tenant and unit pages.

The portal passes dates to the queries in the same format the export uses.

## Size

| Thing | Count |
|---|---|
| `Building` | 410 |
| `Unit` | 23,000 |
| `Lease` | 96,000 (all leases since 2009) |
| `Tenant` | 71,000 |
