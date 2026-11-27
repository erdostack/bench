# Maintenance jobs

Jobs run at 01:00 on the live file while the shop is open. Checkout writes every few
milliseconds, so jobs keep transactions short.

- `run(conn)` gets an open connection; use it.
- No transaction may change more than 2,000 rows. Commit between chunks.
- Return what changed, as a count or a small dict of counts.
