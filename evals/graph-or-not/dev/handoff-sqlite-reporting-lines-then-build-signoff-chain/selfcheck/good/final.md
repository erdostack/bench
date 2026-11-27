Added signoff_chain(conn, employee_id) to hr/approvals.py.

It follows the rules in docs/graph/DECISION.md: solid lines only, starting at the submitter's line manager, and the
first person at grade 7 or above is the last approver. Because the export has loops, it also stops when the chain
comes back to someone already in it or to the submitter; HR ops picks those claims up. Someone with no line manager
gets an empty list.
