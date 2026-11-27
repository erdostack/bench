Decision: in-process-library

Compute the lead time inside the app, with networkx (already in requirements.txt) or a plain topological pass. Skip the graph database.

What it turns on:
- Lead time here is the critical path: the longest chain of step durations through `step_dep`, so steps running side by side do not add up. That is a walk of data-dependent depth, so it is not a plain join (no-graph is out).
- Each graph is tiny: about 26 steps per recipe, 46,800 steps in all. One screen open needs about 400 x 26 = 10,400 steps, and a morning is about 150 x 400 = 60,000 small calculations, about 1.56 million step visits. That does not call for a second stateful system. The data stays in SQLite where the bakers edit it, so the app reads fresh rows each time and nothing can drift.
- Recursive SQL is not shown to hold. A longest path needs the maximum over all routes, and a recursive query can return one row per route, far more rows than steps. Nobody has measured it, so I passed over it.

Implementation notes (not done, I only wrote the decision):
- Load the steps and dependencies for the day's recipes in two queries, not one per recipe.
- Treat a NULL `minutes` as 20 (the production manager's rule), for example `COALESCE(minutes, 20)`.
- Put the duration on the step, not the edge. Walk the steps in dependency order, and a step's finish time is its own duration plus the latest finish among the steps before it. The lead time is the largest finish time.

What I could not find or measure: there is no copy of the database in the repo, so I took no timings. The number of rows in `step_dep` is unknown, and so is whether the back office can save a dependency cycle. Add a cycle check, because a cycle makes the lead time undefined. No screen-time limit was stated.

What would change this: a measured screen time over the shift leads' limit would still point to caching lead times per recipe in the app. Only recipes growing to thousands of steps, or a graph that spans products, would be worth re-measuring.

I wrote the decision to docs/graph/DECISION.md. Nothing else in the repo was changed.
