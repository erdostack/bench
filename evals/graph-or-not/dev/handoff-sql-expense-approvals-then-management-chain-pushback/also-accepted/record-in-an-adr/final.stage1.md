Decision: no-graph. Written up in docs/adr/0007-expense-approval-routing.md.

Finance's policy needs no traversal: the approver is the owner of the report's cost centre (one lookup in
cost_centre), plus the financial controller when the total is over €10,000. It never goes further up the org chart,
whatever the amount, so employee.manager_id is not involved at all; today's routing to the submitter's manager is
simply the wrong lookup. 3,000 cost centres and about 1,200 reports a day are trivial for two indexed lookups. Joel's
graph of the org chart would implement a policy finance does not have.
