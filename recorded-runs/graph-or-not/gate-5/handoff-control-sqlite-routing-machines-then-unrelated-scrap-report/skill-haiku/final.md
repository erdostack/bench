I wrote `sql/scrap_by_machine.sql`. It takes `:day` (YYYY-MM-DD) and returns `machine_id`, `produced` and `scrapped` for each machine that has at least one non-void `prod_log` row on that day, ordered by `machine_id`.

It matches the day with `substr(logged_at, 1, 10)`, so the `YYYY-MM-DD HH:MM` local timestamps are compared on their date part. Rows with status `'void'` are dropped before the grouping, so they add nothing to the sums and a machine with only void rows that day does not appear.

I ran it on a small scratch database built from `db/schema.sql` and then deleted that database. A machine with one void row and no ok rows was left out, and a day with no rows returned nothing.
