I added `sql/scrap_by_machine.sql`. It takes `:day` (YYYY-MM-DD) and returns one row per machine as `(machine_id, produced, scrapped)`, the sums of `prod_log` for that day. Rows with status 'void' are dropped before grouping, so a machine whose only rows that day are void does not appear. Results are ordered by `machine_id`.

The day is matched on the first 10 characters of `logged_at`, which is the date part of the 'YYYY-MM-DD HH:MM' local time.

I checked it on a small in-memory database built from `db/schema.sql`. For 2026-03-02 it returned machine 1 with 15 produced and 3 scrapped, and machine 3 with 5 and 1. Machine 2 was absent because its only row that day was void. For 2026-03-03 it returned only machine 2, and for a day with no rows it returned nothing.
