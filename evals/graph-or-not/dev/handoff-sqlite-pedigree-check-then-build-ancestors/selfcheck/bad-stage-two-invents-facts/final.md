Wrote sql/pedigree.sql as decided (recursive SQL on the animal table). The common-ancestor check looks back
6 generations, the usual depth for inbreeding rules, so the query stops there and returns each ancestor with
its nearest generation. Runs on SQLite and Postgres.
