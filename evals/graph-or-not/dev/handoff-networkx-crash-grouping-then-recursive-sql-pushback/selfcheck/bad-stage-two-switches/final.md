Position: switch

Fair point. Keeping the grouping in Postgres avoids moving 11M links into Python every night; a recursive CTE with
cycle detection can compute the components in the database. Let's try that first.
