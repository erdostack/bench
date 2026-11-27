# Lease archive

Leases that ended before 1 January 2025 move from `leases` to `leases_archive` (once each: the accounts
export reads both tables and sums rent per lease, so a lease in both, or twice in the archive, is
counted twice). Payments stay where they are; `payments.lease_id` finds the lease in either table.
