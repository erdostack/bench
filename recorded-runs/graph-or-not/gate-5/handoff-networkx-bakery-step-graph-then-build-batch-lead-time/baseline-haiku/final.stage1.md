Decision: in-process-library

Lead time is the critical path through each recipe's step graph: the longest chain of dependent steps, weighted by step minutes, with an untimed step counted as 20 minutes. It is a graph problem, but a small one, and it can be answered in memory with networkx (already in requirements.txt) or a plain topological pass.

Why this option:
- The data is small. About 1,800 recipes at about 26 steps each is roughly 47,000 steps, plus their step_dep rows. That fits in memory several times over, and each recipe is a DAG of about 26 nodes.
- A dedicated graph database is far too much for this. It adds a server and a second store, and it does not make a 26-node longest-path any faster.
- Recursive SQL is possible, but a longest-path (max over sums) through a recursive CTE is awkward to write and to verify, and it is easy to get the path explosion wrong. Doing it in code is simpler.
- The screen needs a value for about 400 products, 150 times a morning. Compute each recipe's lead time once per load (or cache it per recipe and refresh when the back office changes a recipe or step), so the screen does not repeat the work on every open.

How to build it:
- Load the steps for the day's recipes and their step_dep edges once.
- Build a directed graph per recipe (networkx DiGraph, or a dict of predecessors). Use the rule that an untimed step (minutes IS NULL) counts as 20.
- Lead time = longest weighted path ending at the last step, computed in topological order. Ignore the steps that do not wait on each other: they run in parallel and only the longest chain sets the time.
- Check for cycles before computing. A cycle in step_dep means a recipe cannot be planned, so flag it on the screen instead of failing the whole morning.

Caveats:
- Nothing was run here, so the numbers and the timing are unverified. Check the result on a few recipes whose steps were timed by hand.
- The 20-minute default is the production manager's rule. It can make lead times look longer than they are for recipes with many untimed steps. Showing how many steps on each line are untimed would help the shift lead trust the figure.
- Jonas's point that recipes are graphs is right, but the graph here is tiny, so the decision is about cost and simplicity, not about whether a graph is present.
