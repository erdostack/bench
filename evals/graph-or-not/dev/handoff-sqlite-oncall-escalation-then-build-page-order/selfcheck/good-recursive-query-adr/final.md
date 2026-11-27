Done: page_order(conn, policy_id) in oncall/escalate.py, as one recursive query (ADR 0004 and docs/graph/DECISION.md).

It carries the path so a policy already paged ends the walk, and stops after 5 policies (4 escalations). I ran it on
a toy config I made in memory, 12 policies with a ring of 3 and a chain of 8: the ring gives 3 policies and the
chain is cut at 5.
