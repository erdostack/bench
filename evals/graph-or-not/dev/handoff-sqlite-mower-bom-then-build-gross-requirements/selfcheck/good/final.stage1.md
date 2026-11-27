Decision: recursive-sql

Gross requirements are a walk down at most 11 levels of 210,000 BOM lines, about 300 times a day with 3 s
allowed, and your recursive query already does the biggest ride-on mower in 0.4 s. A graph database would be a
second copy of the PLM data to keep in sync for a walk Postgres already answers. One recursive query per order,
multiplying qty_per down the lines with the 4% scrap per line compounding, summed per bought-in part.

I wrote this down in docs/graph/DECISION.md, including the scrap rule, since the schema has no column for it.
