I added `ovenplan/leadtime.py` with `lead_time(conn, recipe_id)`. It returns the minutes from the first step starting to the last step finishing. Each step starts when every step it waits on (`step_dep`) has finished, and steps that don't depend on each other run in parallel. So the result is the longest chain of dependent steps. I tested it on a small in-memory database with a diamond-shaped set of dependencies and an independent long step. I haven't hooked it into the screen.

I couldn't find "the way we decided" anywhere in the repo, so I made these choices myself. Please check them against what you decided:

- **Untimed steps:** `step.minutes` is NULL until someone times the step, and the bakers edit the data live. I didn't treat NULL as 0, because that would show a lead time that is too short. Instead `lead_time` raises `LeadTimeError` ("steps not timed yet: ...") naming the steps. When you wire it in, the screen has to catch that and show something like "not timed" instead of a number. If you decided on a different rule, such as counting NULL as 0, it's a one-line change.
- **Circular dependencies:** these also raise `LeadTimeError`, and the check runs only when the recipe's steps are scheduled.
- **No steps:** a recipe with no steps, or an unknown `recipe_id`, returns 0.
- **Batches:** the result is the lead time for one batch. `daily_plan.batches` is not used.
