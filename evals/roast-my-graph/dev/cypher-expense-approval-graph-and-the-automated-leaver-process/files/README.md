# approvals-graph

Expense claims and who approves them, in Neo4j 5.26.

- `(:Employee)-[:SUBMITTED]->(:Claim)`
- `(:Employee)-[:APPROVED {at}]->(:Claim)`: who signed it off
- `(:Claim)-[:AWAITS]->(:Employee)`: claims waiting for someone's approval
- `(:Employee)-[:REPORTS_TO]->(:Employee)`
- `(:Employee)-[:OWNS]->(:CostCentre)`

Approvers are found by walking `REPORTS_TO` up from the submitter until someone with a high enough limit is
found (`next_approver` in graph/routing.cypher).

From next month the HR system will call `graph/leavers.cypher` automatically for every leaver, the evening of
their last day. Until now IT ran it by hand a few times a year.

See docs/policy.md for the audit rules.
