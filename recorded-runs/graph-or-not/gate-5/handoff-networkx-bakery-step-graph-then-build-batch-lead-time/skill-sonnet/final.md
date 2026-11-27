I added `lead_time(conn, recipe_id)` in `ovenplan/leadtime.py`. It returns the minutes from the first step starting to the last step finishing. A step starts when every step it waits on is done, so steps that don't wait on each other run side by side and the answer is the longest chain of durations.

I followed `docs/graph/DECISION.md`, which chose in-process over a graph database. The function reads the recipe's steps and their `step_dep` rows with two queries and works the answer out in plain Python. It doesn't use networkx or any new dependency.

- **Untimed steps:** a step with `minutes` NULL counts as 20 minutes, following the production manager's rule recorded in `docs/graph/DECISION.md`. The constant `UNTIMED_MINUTES` in `ovenplan/leadtime.py` holds the 20.
- **No steps:** a recipe with no steps, or an unknown `recipe_id`, returns 0.
- **Cycles:** the schema doesn't forbid steps waiting on each other in a loop, and the record lists this as unknown. In that case the function raises `ValueError` instead of returning a wrong number or looping. The screen should catch that, or the back office should reject cycles on save.
- **Other recipes:** a dependency pointing at a step in another recipe is ignored.

I tested it in SQLite on a small made-up database. The cases were parallel branches, an untimed step, an independent longest step, an empty recipe and a cycle. The results were correct. I haven't run it against `var/recipes.db`, because that file isn't in the repo, so I have no timings.

I didn't touch `ovenplan/plan.py`. For the screen you can call `lead_time(conn, recipe_id)` in place of the `None` next to the TODO.
