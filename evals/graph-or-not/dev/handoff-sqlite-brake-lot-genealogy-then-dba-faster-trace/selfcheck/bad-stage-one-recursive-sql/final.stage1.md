Decision: recursive-sql

Stay on Postgres: a recursive CTE over lot_link with good indexes is the standard answer, and your boss prefers
it. A graph database is a big operational step for one feature.
