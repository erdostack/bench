# ovenplan

Production planning for the bakery: what to make, when to start it, which oven.

- Python 3.12, Flask. Data is one SQLite file (`var/recipes.db`, schema in `db/schema.sql`) that the bakers edit
  through the back office.
- `ovenplan/plan.py` builds the morning planning screen.
