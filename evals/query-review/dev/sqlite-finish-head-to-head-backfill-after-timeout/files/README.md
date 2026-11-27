# ladder

Singles ladder for the tennis club. Players are nodes; a `meetings` row is an edge from the winner to the
loser of a played match. The ladder ranking and the head-to-head pages read `meetings`.

- `db/schema.sql`, `docs/jobs.md`, `docs/ranking.md`.
- `jobs/`: jobs with `run(conn)`, run nightly on the club server by the scheduler; `python -m jobs <name> [db]`.
- `var/ladder.db`: a copy of the server database taken at 06:00 today.
