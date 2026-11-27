# squadup

Matchmaking data for the game's "play again with" list. `played_with` is the who-played-with-whom
graph: one row per unordered pair of players (a < b). `var/squadup.db` is a copy of the live database
(`db/schema.sql`).

- `jobs/`: maintenance jobs with `run(conn)`; `python -m jobs <name> [db]`. Rules: `docs/jobs.md`.
- `docs/clients.md`: what each client sends to the sync service.
