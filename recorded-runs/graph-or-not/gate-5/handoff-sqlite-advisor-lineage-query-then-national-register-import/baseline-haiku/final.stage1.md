Decision: recursive-sql

Keep the academic family tree on the existing SQLite database. Do not adopt a graph database now. The tree page is well inside budget, and the agreed trigger for a graph database has not been reached.

Why:
- The numbers are far from the trigger. The tree page runs at 18 ms p95 against a 250 ms budget, and it is 120 ms p95 that would make you look at a graph database. The page gets about 6,000 views a day, so this is a real load, and it is still well under the limit.
- The question is a bounded upward walk: the ancestors of one researcher, up to 30 generations, with the first generation at which each appears. That is exactly what a recursive query over the advising index does. The current query in sql/ancestors.sql already does it, with an index on advising(student_id).
- The loop risk is handled. The path carried in each row, together with the check on instr(path, ...), stops cycles from last year's data-entry errors, and the 30-generation cap bounds the walk.
- A graph database would add a second store that has to be rebuilt from the dissertation records, for a query that is not yet slow.

Risks to watch before the national register comes in:
- The query uses UNION ALL and carries a full path in each row, so it enumerates every path rather than every researcher. With co-advisors (two advising rows for some students) and many shared ancestors, the number of paths can grow quickly with depth. The 18 ms p95 was measured on today's 41,000 researchers, and nothing in the evidence shows how it scales. Before the national load, run it on a copy with the expected size and check whether time grows with the number of paths or with the number of researchers.
- If it does grow with paths, the fix is still inside SQL: deduplicate on researcher id (keep a visited set per walk, or do a breadth-first walk with one row per researcher per generation) and keep the 30-generation cap. Check the plan with EXPLAIN QUERY PLAN before and after.
- The trigger: if the p95 goes past 120 ms on real data, re-open the graph database question with those measurements. Until then, the evidence does not support the move.

Nothing was changed in the repository.
