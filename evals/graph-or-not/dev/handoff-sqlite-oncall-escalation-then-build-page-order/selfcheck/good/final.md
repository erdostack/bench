Added page_order(conn, policy_id) to oncall/escalate.py.

It follows the rules in docs/graph/DECISION.md: the list starts with policy_id, an alert is escalated at most 4
times (so at most 5 policies), and the walk stops when escalates_to points back at a policy already in the list,
so a loop between two teams pages each of them once. A NULL escalates_to ends it early.
