sql/controlled_companies.sql is in.

From ADR 0012: control means 25% or more at every step, chains are at most 9 companies, and there are loops in the
holdings. The recursion stops after 9 steps, which both ends the loops and covers every chain on record, and the
outer query keeps the fewest steps per company and drops the client's company.

If a chain longer than 9 ever turns up, the bound in the query is the one number to change.
