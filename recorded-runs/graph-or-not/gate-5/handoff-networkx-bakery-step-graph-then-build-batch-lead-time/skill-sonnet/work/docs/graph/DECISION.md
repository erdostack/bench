# Graph decision

Decision: in-process-library

The planning screen needs the lead time of each product: the time from the first step starting to the last step finishing, where steps that do not wait on each other run side by side. That is the longest chain of durations through the step dependencies of one recipe (the critical path), which is a walk over a graph with a depth that depends on the data, but each graph is small: about 26 steps per recipe, about 46,800 steps in all. The work is done inside the Flask app on the rows of today's recipes, with networkx (already pinned in requirements.txt) or a plain topological pass, and no graph database is needed.

## Workload facts

- 1,800 recipes, about 26 steps each (stated by the user)
- Total steps = 1,800 x 26 = 46,800 steps (stated by the user, multiplied out)
- Steps wait for earlier steps through `step_dep`; steps that do not wait on each other run side by side (stated by the user; db/schema.sql, table `step_dep`)
- Question asked: lead time = longest path of step durations from first start to last finish within one recipe, a data-dependent depth over one relation between steps of the same kind (stated by the user; `step_dep.before_id` and `after_id` both reference `step`, db/schema.sql)
- About 9% of steps have never been timed (`step.minutes` is NULL); the production manager's rule is that an untimed step counts as 20 minutes until it is timed (stated by the user). Untimed steps = 0.09 x 46,800 = about 4,200 steps, and the rule belongs in the code that reads `minutes` (db/schema.sql for the NULL, rule stated by the user).
- Load: the shift lead opens the screen about 150 times a morning and each time it works out about 400 products (stated by the user). That is 150 x 400 = 60,000 lead-time calculations a morning, each over about 26 steps, so about 60,000 x 26 = 1.56 million step visits a morning if nothing is cached.
- Rows loaded per screen = 400 x 26 = about 10,400 steps plus their dependencies, a small fraction of the 46,800 in the file (stated by the user, multiplied out)
- The only code path is `screen()` in ovenplan/plan.py, which loops over `todays_products` and has a TODO for the lead time; `lead_time` is `None` today (ovenplan/plan.py)
- Data is one SQLite file that the bakers edit through the back office, read fresh by the app on each screen open (README.md, ovenplan/plan.py `sqlite3.connect(DB)`)
- Operated today: Flask on Python 3.12 and one SQLite file, networkx 3.7 pinned (README.md, requirements.txt)
- Memory: the whole step table is 46,800 rows; even at a generous 1 KB per node and edge in a Python graph that is under 50 MB, and the screen needs only about 10,400 steps at a time (arithmetic from the stated counts; the bytes per node are an assumption and were not measured)
- unknown: the number of dependency rows in `step_dep` (the average steps each step waits for); there is no database copy in the repo, so nothing was measured
- unknown: whether the back office can save a dependency cycle (nothing in the schema forbids one; no code or migration for the back office is in this repo)
- unknown: how long the screen may take to open; no latency requirement was stated
- Nothing was measured; there is no copy of `var/recipes.db` in the repo and no timing for any option.

## Options considered

- graph-database (the dedicated graph database Jonas wants): rejected, because the data is 46,800 steps edited in SQLite by the bakers, each calculation touches only about 26 steps, and the load is 60,000 small calculations a morning, so there is no size, depth or concurrency that a second stateful store would remove.
- in-process-library (networkx, already in requirements.txt): chosen, because each recipe is a small graph (about 26 steps), the 400 products on screen need about 10,400 steps loaded in two queries, and the walk runs in the app on fresh rows so there is nothing to keep in step with the back office. A plain topological pass in Python gives the same answer without the library.
- recursive-sql (recursive CTE in SQLite): rejected, because it is not shown to hold: a critical path needs the maximum over all routes, and a recursive query that carries one row per route can return far more rows than there are steps when steps fan out and join back. No measurement was taken, and the app-side pass avoids the question.
- no-graph (plain joins): rejected, because a plain join cannot give the lead time; the longest chain of dependent steps needs a walk over `step_dep` to a depth that varies by recipe, and summing all durations would overstate the time for steps that run side by side.

## What would change the decision

- A recipe import that creates dependency cycles would need a check before the calculation (a cycle makes the lead time undefined); the back office owner decides whether to reject them on save.
- A screen open time over the limit the shift leads set (nobody has stated one) with the calculation measured as the main cost would move this to caching the lead times per recipe and recomputing when the recipe is edited, which stays in-process-library.
- Recipes growing from about 26 steps to thousands of steps each, or the load rising far above 60,000 calculations a morning, would be worth re-measuring; it would not move to graph-database unless SQLite itself became the bottleneck.
- The lead time needed across products (a step shared between recipes, or one recipe's output feeding another) would make the graph larger than a recipe; then the edge count should be summed again against the memory of the Flask process.
