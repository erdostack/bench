# Operations

- Deletes of more than about 100,000 nodes must be batched with `CALL { } IN TRANSACTIONS` (or split
  into repeated bounded runs). Smaller ones run as a single transaction.
- Statements run from the app go through the driver's managed transactions (`execute_read` /
  `execute_write`) unless a comment in the code says otherwise.
