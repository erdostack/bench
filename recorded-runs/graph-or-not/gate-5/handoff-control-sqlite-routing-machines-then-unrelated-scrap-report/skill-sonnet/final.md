I wrote `sql/scrap_by_machine.sql`. It takes `:day` and returns `(machine_id, produced, scrapped)`, ordered by `machine_id`.

- **Void rows:** the query drops every `void` row before grouping, so they add nothing to the sums. A machine whose only rows that day are void doesn't appear.
- **Day boundary:** `logged_at` is local time, so the day is matched as written, with no timezone conversion. The filter is `logged_at >= :day AND logged_at < date(:day, '+1 day')`. A row at `23:59` counts for that day, and one at `00:00` belongs to the next.

I checked it in SQLite against a small made-up set of rows. The set had void rows, rows on the neighbouring days and a machine with only void rows. The results were correct, and a day with no rows returns nothing. I didn't have `var/plant.db`, so I haven't run it on real data.

This was plain aggregation, so the `graph-or-not` skill didn't apply. I left `docs/graph/DECISION.md` and everything else alone.
