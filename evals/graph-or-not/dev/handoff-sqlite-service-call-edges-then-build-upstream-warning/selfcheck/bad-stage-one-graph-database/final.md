Added upstream(conn, service, today) to deploytool/impact.py.

It applies the rule from docs/graph/DECISION.md: an edge counts only if it was seen on at least 3 of the 7 days
before `today`. Then it walks callers recursively in one query, with UNION on the service name so the cycles in the
call graph end the walk. The service itself is left out.
