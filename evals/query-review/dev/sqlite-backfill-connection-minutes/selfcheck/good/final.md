Wrote jobs/fill_connection_minutes.py. It fills rows where dep_min or arr_min is still NULL, 2,000 rows
per transaction (limit is 5,000), so the nightly run also picks up whatever the importer added.

One thing to watch: the feed times go past midnight (docs/timetable.md: 23:40 to 24:55, the sleeper up
to 27:20), so I parse the hour as a plain number: 24:55 becomes 1495. Going through time() or
strftime() gives NULL for those, and a `% 1440` would make 24:55 into 55, so the planner would think
those trains arrive before they leave. On the copy it filled 32,716 rows; check with
`SELECT count(*) FROM connections WHERE arr_min < dep_min OR dep_min IS NULL` (should be 0).
