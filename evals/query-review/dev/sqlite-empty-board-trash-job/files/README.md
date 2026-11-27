# pinboard

Whiteboards made of cards. Cards are joined by connectors (arrows) and grouped into frames (a frame is
itself a card). `var/pinboard.db` is a copy of the live database; `db/schema.sql`; `docs/model.md`.

- `jobs/`: nightly jobs, `run(conn)`; `python -m jobs <name> [db]`. Rules in `docs/jobs.md`.
