I added `sql/late_departures.sql`. It takes `:service_date` and returns `service_id` and `station_code` for each departure that ran and left 5 or more minutes after its scheduled time. It matches the style of `sql/cancellations.sql`, including `date(scheduled) = :service_date` and the same ordering.

- **Ran:** `actual IS NOT NULL`.
- **Late:** `strftime('%s', actual) - strftime('%s', scheduled) >= 300`, so exactly 5 minutes counts. Comparing in seconds also gets a departure scheduled late at night that leaves after midnight right.
- **One row per departure:** the query reads only the `departure` table, whose primary key is `(service_id, station_code)`, so no row can appear twice.

I tested it on a small in-memory SQLite database built from `db/schema.sql`. With a service date of 2025-03-01, a delay of 4 minutes was excluded and a delay of exactly 5 minutes was included. A late-night departure that left after midnight was included. A cancelled departure (`actual` NULL), an early departure and a departure on another date were excluded. I couldn't run it on the real `var/rail.db` because it isn't in the repo.

This is a plain filter with no graph traversal, so I made no graph decision. I left `docs/graph/DECISION.md` and all other files unchanged.
