Added sql/controlled_companies.sql, following the recursive-sql decision in docs/graph/DECISION.md.

Control is the usual majority rule: more than 50% of the shares at each step. The query walks holding with that
filter, stops after 20 steps as a safety net, and returns each controlled company with its fewest steps, leaving
the client's own company out.
