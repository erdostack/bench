Decision: recursive-sql

The benchmark in docs/perf answers this: the recursive query is 4.2 ms p95 today and 6.8 ms p95 with the regional
editions' 19,000 tags at 2,100 req/s, against a 250 ms tag-page objective and a 120 ms review line for any single
query (docs/slo.md). A graph database would be a second copy of the taxonomy for a query with almost 18x headroom
on the projection. Written up in docs/graph/DECISION.md.
