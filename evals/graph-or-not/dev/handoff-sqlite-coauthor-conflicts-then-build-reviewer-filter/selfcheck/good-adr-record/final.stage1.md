Decision: recursive-sql

Stay on Postgres; this needs no new store. Strictly there is nothing recursive here: the rule stops at direct
co-authors, so it is a single join. Recorded in docs/adr/0021-conflict-of-interest-filter.md.

Rule: co-authored with any submission author within 24 months; direct only; institutions irrelevant.
Size: 5.2M authorship rows, 1,800 submissions a month, picker under a second. That is an indexed join.
