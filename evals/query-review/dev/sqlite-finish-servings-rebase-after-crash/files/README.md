# pantry

Recipe graph behind the cooking app: recipes, ingredients, and `uses` edges (recipe -> ingredient,
with a quantity and a unit). `var/recipes.db` is a copy of the live database; `db/schema.sql`.

- `jobs/`: data jobs with `run(conn)`; `python -m jobs <name> [db]`. Rules in `docs/jobs.md`.
- `logs/`: job logs copied from the scheduler.

The 2019 partner import (source `2019-import`) stored every recipe for 12 servings, whatever the
original said. RCP-311 rebases them to 4 servings, the app's default.
