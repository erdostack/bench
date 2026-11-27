# letwell

Property management for our rental units. Neo4j 5.26.

    model/model.md           labels and relationships
    model/schema.cypher      constraints
    queries/leases.cypher    arrears report, tenant page, payments

## How leases work here

A lease is signed by one to four tenants (co-tenants share one lease and are jointly liable). Rent is
paid against the lease, not against a tenant: a payment can come from any co-tenant, a guarantor or a
housing benefit office. A deposit is held for a lease and returned when it ends. A guarantor
guarantees a lease.

## Sizes

6,200 units, 14,000 tenants, 21,000 leases (current and past), 1.1 million payments, 19,000 deposits,
3,100 guarantors.

The arrears report runs every morning; new leases (started in the last 90 days) are checked by the
onboarding team instead.
