# Account hierarchy for invoicing

Decision: recursive-sql

A recursive query on Postgres walks the account hierarchy for the monthly run. The data is small and the run is a
batch job, so a graph database is not justified.
