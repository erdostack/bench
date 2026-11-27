# threadline

Discussion boards. Every post is a node, `parent_id` points at the post it replies to (NULL for the
first post of a thread). `var/threadline.db` is last night's copy of the live database; schema in
`db/schema.sql`, changes in `db/migrations/`.

- `jobs/`: maintenance jobs, one module each, `run(conn)`; rules in `docs/jobs.md`
- `docs/moderation.md`: what moderators can do to threads
- tests: `python -m unittest discover -s tests`

    python -m jobs list
    python -m jobs run close_stale_threads [path/to/db]
