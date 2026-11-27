# Field day checklist

1. Export the day's sheet from the tablet as CSV into `data/`.
2. `uv run birdlog load data/` (this rebuilds everything; it takes a few seconds).
3. `uv run birdlog query queries/first_dates.cypher` and read out any new arrivals at the debrief.

Only the group secretary runs step 2.
