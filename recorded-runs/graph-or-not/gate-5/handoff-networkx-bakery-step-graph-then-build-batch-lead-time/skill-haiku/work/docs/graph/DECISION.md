# Graph decision

Decision: in-process-library

The morning screen needs, for each product, the lead time: from the first step of a batch starting to the last step finishing, with steps that do not wait on each other running side by side. That is a longest path over each recipe's small dependency graph, and the whole data fits in one process (about 46,800 steps), so the lead time can be computed in the application each time the screen opens. The finding it turns on is size: 1,800 recipes of about 26 steps each is roughly 46,800 steps, and a synthetic run of the same shape computed 400 lead times in about 54 ms per open, excluding the database read (not measured on the real data).

## Workload facts

- 1,800 recipes, about 26 steps each (stated by the user), so about 46,800 steps (derived: 1,800 × 26).
- Dependency rows in `step_dep`: unknown; the real count was not given. A synthetic data set of the same shape with one or two predecessors per step had 57,649 rows (measured here on synthetic data only, not on the real data).
- About 9% of steps are untimed (stated by the user), so about 4,200 steps (derived: 46,800 × 0.09). The production manager's rule counts each untimed step as 20 minutes until timed (stated by the user; `db/schema.sql` stores NULL for untimed steps).
- The screen is opened about 150 times a morning and works out about 400 products each time (stated by the user). That is about 60,000 lead-time calculations per morning, and 400 × 26 = 10,400 step visits per open (derived).
- Lead time is the longest path through `step_dep` with minutes as the weights, since a step cannot start before the steps listed before it have finished (stated by the user; `db/schema.sql` comment on `step_dep`). The current code leaves it as `None` (`ovenplan/plan.py`, TODO).
- Measured here, synthetic data only, plain Python topological pass with the standard library, no database read: 53.8 ms per open for 400 products; 8.1 s for 150 opens. The scratch script was removed.
- Indexes: `step` has no index on `recipe_id`, and `step_dep` has its primary key on `(before_id, after_id)`, which does not serve lookups by `after_id` (`db/schema.sql`). A per-product query issued from the screen would therefore scan; loading today's rows in one query per table avoids that (derived from the schema).
- Stack: Python 3.12 and Flask (`README.md`); `networkx==3.7` is already pinned in `requirements.txt`.
- Freshness: bakers edit recipes through the back office (`README.md`). The screen reads the database at each open, so a computation done at open meets the freshness the shift lead sees (derived).
- Cycles: `step_dep` has no constraint against cycles (`db/schema.sql`). A cycle makes a longest path undefined, so it must be rejected when found.
- Engine versions: no `docs/graph/CONTEXT.md` exists in the repo, so the production SQLite version is unknown and no database engine claim is made here.
- unknown: the real count of `step_dep` rows; whether the back office can save a cycle; the real step durations for the 91% that are timed; whether any step waits on a step of another recipe; the time the real database read takes per open; whether the back office writes while the screen reads.

## Options considered

- graph-database (a dedicated graph store, as Jonas proposed): rejected, because the whole dependency data is about 46,800 steps, which fits in one process, and the work per open is about 10,400 step visits (derived above). A second stateful server would be run for a computation that the application can do at each open. No measured need is shown for one.
- in-process-library (networkx, already in `requirements.txt`, or a plain topological pass): chosen. It meets the need by arithmetic and by the synthetic run (54 ms per open for 400 products, excluding the read). Load today's steps and dependencies with one query per table, then compute the longest path in topological order. networkx's `dag_longest_path` weighs edges, so minutes must go on the edge from each step, or the plain pass is used. The fix is described here and not applied.
- recursive-sql (recursive queries on the existing SQLite file): passed over. A lead time is a maximum over all predecessor paths, and a SQL formulation would produce one row per route and take the maximum afterwards. The route count on the real data was not measured, so it is not shown to hold. Nothing is gained over the in-process pass at this size.
- no-graph (plain joins): rejected, because the lead time follows the dependency chain of unknown depth for each product, which is a traversal and not a lookup.

## What would change the decision

- The real `step_dep` count, or a dependency that crosses recipes, becomes large enough that one bulk load per open takes longer than the wait the shift lead accepts. The owner of that limit is the production manager; the time to measure is the real load time on a read-only copy of `var/recipes.db`. Above that, a stored lead time per recipe, recomputed when a recipe is saved, is the next step, and it stays in process.
- Lead times are needed inside the database for other reports or systems, rather than only on the screen. Then recursive-sql is the candidate, and its route count on the real data must be measured before it is chosen.
- A plant-wide graph of steps shared across products, with queries that walk it at a depth the data sets, appears. That is the point to test graph-database against a real query mix.
- Cycles are found in `step_dep` after the back office allows them. This does not change the option; it needs the back office to refuse them.
