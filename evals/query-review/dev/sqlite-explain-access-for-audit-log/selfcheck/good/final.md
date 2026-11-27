Added explain_access to app/access.py. It walks the nesting breadth-first from the user's own groups, one level per
query, and keeps the first group it reached each group from, so the first grant holder it meets ends a shortest
chain. Nesting loops back on itself in the real data and there are many routes to the same group; a recursive SQL
query that carries the path would have to list every route and does not finish. On var/access.db the longest
shortest chain I saw was 10 groups, and each call takes a few milliseconds. can_access is unchanged.
