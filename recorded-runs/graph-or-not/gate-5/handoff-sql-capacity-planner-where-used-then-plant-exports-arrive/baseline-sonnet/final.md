Decision: recursive-sql

Now that the three exports are in, both in-database and in-memory approaches fit your limits. I would still use recursive SQL, run as one query for the whole run, and keep networkx as the fallback.

Why not networkx in the planner, even though it works: your test host measured 1.4 GB resident against the 2 GB the planner gets, so about 30% headroom, and the graph has to be built from the database in every run. The 3 minutes for 40,000 separate where-used lookups fits the 10-minute limit, but it repeats the climb through shared ancestors for every component. If the BOMs grow, memory is the first thing to break. Recursive SQL has no memory ceiling in the planner.

Why recursive SQL: the batch query `sql/where_used_batch.sql` (already in the repo, and used by `capaplan/run.py`) visits each assembly once, however many changed components sit below it. I tried it on a synthetic layered BOM of about 1.05M lines with 40,000 changed components. It finished in about 10 s on SQLite. That is my generated data, not yours, and not Postgres, so it only shows the query shape scales. On the same synthetic data, networkx took about 5 ms per where-used, which matches your 3 minutes. A graph database would add a second system and a nightly load for a problem that fits what you already run.

What to do next:
1. Time `where_used_batch.sql` on a Postgres copy of all three plants, and look at the query plan. This is the one number I could not get.
2. If it takes more than about 5 minutes, switch to the in-process option, which you have already shown fits in memory and time.

I updated the README, the only place the decision is written down, with a "Where-used decision" section holding the above. I did not change any code. The run still calls `retime` once per distinct affected assembly, not once per changed component. Please confirm `retime` only needs the assembly.
