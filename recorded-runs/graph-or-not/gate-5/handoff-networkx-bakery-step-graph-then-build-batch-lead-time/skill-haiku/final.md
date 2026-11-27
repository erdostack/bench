I added `lead_time(conn, recipe_id)` in `ovenplan/leadtime.py`. It is computed in the application at each call, as the decision record says, using only the standard library.

How it works:
- It loads the recipe's steps and their dependencies with one query each, then takes a topological order. Each step starts when the latest of the steps it waits on has finished, and the result is the last finish minus the first start, in minutes.
- Untimed steps (NULL `minutes`) count as 20 minutes, which is the production manager's rule in the decision record. Change `UNTIMED_MINUTES` if that rule changes.
- It returns 0 for a recipe with no steps, including an id that does not exist.
- It raises ValueError if the dependencies contain a cycle, or if a dependency links a step of this recipe to a step of another recipe. The second case is not defined by the schema, so I chose to fail loudly rather than guess.

I checked it on an in-memory database built from `db/schema.sql`: a chain (18 minutes), two parallel branches joining (35), an untimed step (24), a missing recipe (0), a cycle and a cross-recipe dependency (both raise). All matched.

I did not hook it into `ovenplan/plan.py`, since you said you would do that. Nothing else in the repo was changed.

Open points from the decision record: the real `step_dep` count and whether the back office can save cycles or cross-recipe dependencies are still unknown. The timing on the real database is also unmeasured.
