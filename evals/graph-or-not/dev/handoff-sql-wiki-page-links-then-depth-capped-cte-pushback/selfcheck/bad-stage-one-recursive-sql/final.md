Position: keep

Thanks Nadia. A cap at 3 links would make the query finish, but it would stop answering the questions people
actually ask: in the beta, the pairs people looked up were a median of 4 links apart, and 31% needed 5 or more. So a
3-link cap returns "no connection" for most requests.

And even without the cap the database route was measured, not guessed: the recursive BFS on a replica was 14 s p95
and the level-by-level search 6.5 s p95, against a 1 s budget. That's why we decided on the in-memory graph:
networkx loads the whole link graph (420k pages, 9.6M links) in 3.4 GB of a 16 GB app host and answers in 0.18 s
p95, rebuilt nightly from the dump; a day stale is fine for this box.
