I added `ovenplan/leadtime.py` with `lead_time(conn, recipe_id)`. It returns the minutes from the first step starting to the last step finishing. A step starts as soon as every step it waits on, from `step_dep`, is done. The function uses a topological pass over the recipe's steps and does not need networkx.

Three cases do not return a number:
- A recipe with any untimed step (`minutes` NULL) returns None, because the lead time is not known yet. This matches the `lead_time: None` placeholder in `ovenplan/plan.py`, so the screen can show it as unknown.
- A recipe with no steps returns None.
- A dependency cycle raises ValueError. The schema does not prevent cycles, so the screen should catch this if it can happen.

I checked it on a small in-memory database built from `db/schema.sql`. Steps A (10 min) and B (5 min) start together, C (7 min) waits on both, and D (3 min) waits on B. The function returned 17, which matches a hand calculation: C runs from minute 10 to 17. The untimed recipe returned None, the recipe with no steps returned None, and adding a cycle raised ValueError.

Not done: I did not hook it into `ovenplan/plan.py`. You said you would do that.
