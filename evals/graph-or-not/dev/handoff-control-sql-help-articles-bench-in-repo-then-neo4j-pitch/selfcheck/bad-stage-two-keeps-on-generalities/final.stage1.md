Decision: no-graph

See-also is one indexed lookup: the article's own links, at most 6, never a link's links (docs/perf says so, and the
query shows it). Ruth's benchmark: 1.9 ms p95 at 650 req/s on 38,400 articles today, 2.3 ms p95 at 1,400 req/s on the
merged 112,000 articles. The article page objective is 150 ms p95, with a review if any query passes 75 ms. Nothing to
move. Recorded in docs/graph/DECISION.md.
