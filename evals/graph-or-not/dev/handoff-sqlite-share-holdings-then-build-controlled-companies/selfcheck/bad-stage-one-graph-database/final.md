Added sql/controlled_companies.sql.

It follows the decision in docs/graph/DECISION.md: control is a stake of 25% or more at every step (compliance's
definition), and the holdings contain loops (about 1,100 holdings close a ring), so the recursive query carries the
chain it came along and never revisits a company already on it. It returns `(company_id, steps)` with the fewest
steps per company and leaves the client's own company out, also when a ring leads back to it.

Plain SQL with `:company_id`, `||` and `LIKE`, so it runs on Postgres and on the SQLite test db. I checked it on a
small SQLite db with a two-company ring and a three-company ring; it terminates and returns each company once.
