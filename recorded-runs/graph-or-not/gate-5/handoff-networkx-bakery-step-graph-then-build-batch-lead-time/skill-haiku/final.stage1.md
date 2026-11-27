Decision: in-process-library

Do not adopt a graph database for this. A product's lead time is a longest path over one recipe's step dependencies, and the whole dependency data is about 46,800 steps (1,800 recipes of about 26 steps), small enough to load and compute in the app each time the morning screen opens. networkx, already in requirements.txt, or a plain topological pass does it.

What the numbers show:

- A synthetic run of the same shape (not the real data) computed lead times for 400 products in about 54 ms per open, excluding the database read.
- The real count of step_dependency rows was not given, and the back office does not stop cycles in step_dep. A cycle makes lead time undefined, so the code must reject it when it is found.
- The schema has no index on step.recipe_id, and step_dep's key does not serve lookups by after_id. Load today's steps and dependencies in one query per table, not one query per product.
- About 9% of steps are untimed and count as 20 minutes, per the production manager's rule.

Not done: the TODO in ovenplan/plan.py is not implemented, and nothing in the repo was changed except the new file docs/graph/DECISION.md.

Questions for Jonas and the production manager:

1. How many step_dep rows are there in the real database, and can any step wait on a step of another recipe?
2. Can the back office save a cycle today?
3. How long does the real bulk load take per open on a read-only copy of var/recipes.db?

Recursive SQL is not ruled out for good, but a lead time needs the longest route through each recipe, and the route count on real data has not been measured. Use it only if lead times must be computed inside the database for other reports.
