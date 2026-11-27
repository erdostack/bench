Decision: recursive-sql

## Workload facts
- 318.2 million links, 44.1 million accounts.
- ring_check mean 59 ms; 4.2% cancelled at the 400 ms timeout.

## Options considered
- Graph database: a new stateful system for a problem Postgres already mostly solves (95.8% of checks
  succeed). Not worth the operational cost.
- Keep the recursive CTE and tune: partition `links` by entity kind, add a covering index, lower the
  degree cap, and raise the timeout slightly. Chosen.

## What would change the decision
- Timeouts above 10% after tuning.
