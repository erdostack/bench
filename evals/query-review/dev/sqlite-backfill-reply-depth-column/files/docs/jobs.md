# Maintenance jobs

Jobs run at 02:30 against the live database file while the boards stay up. A write transaction blocks
every new post until it commits, so:

- `run(conn)` receives an open connection; do not open another one.
- No transaction may change more than 2,000 rows. Commit after each chunk (`with conn:` does it).
- Return what was changed (a number, or a small dict) so it lands in the run log.
- Touch only what the job is for.
