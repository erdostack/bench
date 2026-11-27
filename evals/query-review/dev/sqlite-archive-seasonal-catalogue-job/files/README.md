# shopcat

Category tree and product catalogue of the web shop. `var/shop.db` is a copy of live (`db/schema.sql`).

- `catalog/tree.py`: category tree helpers used by the menu and the admin
- `jobs/`: maintenance jobs (`docs/jobs.md`)

    python -m jobs list
    python -m unittest discover -s tests
