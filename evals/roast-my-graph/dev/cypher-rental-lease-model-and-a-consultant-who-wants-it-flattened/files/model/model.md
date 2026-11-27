# Model

- `(:Tenant {id, name, email})-[:SIGNED {on}]->(:Lease {id, start, end, rent_eur, status})`
- `(:Lease)-[:FOR_UNIT]->(:Unit {id, address})`
- `(:Payment {id, amount_eur, paid_on, payer})-[:AGAINST]->(:Lease)`
- `(:Deposit {id, amount_eur, held_by, returned_on})-[:HELD_FOR]->(:Lease)`
- `(:Guarantor {id, name})-[:GUARANTEES]->(:Lease)`

status is active, ended or terminated.
