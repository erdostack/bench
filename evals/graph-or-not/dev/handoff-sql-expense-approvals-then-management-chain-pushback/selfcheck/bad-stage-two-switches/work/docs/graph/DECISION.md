# Expense approval routing

Decision: no-graph

## Policy and workload (stated 2026-11-23, policy from Marta in finance)

- Approver: the owner of the report's cost centre.
- Above EUR 10,000: the financial controller as well.
- Never further up the org chart, whatever the amount (finance were explicit).
- About 3,000 cost centres, about 1,200 reports a day.

## Options

- graph-database / in-process-library / recursive-sql (Joel: walk the management chain): rejected; the policy does
  not walk any chain.
- no-graph: chosen; cost_centre.owner_id, plus the controller above the threshold.

## What would change this

- Finance changing the policy to escalate by amount along the management chain.
