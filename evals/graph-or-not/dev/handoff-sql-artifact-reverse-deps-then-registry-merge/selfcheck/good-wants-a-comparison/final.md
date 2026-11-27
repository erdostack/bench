Still stands: no

We kept it in-process on the condition that the graph stays under half of a 32 GB host. It went from 6 GB to
21 GB resident with the merge, so that condition is gone, even though p95 (45 ms vs 38 ms) is fine. The agreed
next step is a graph database; I've marked the record need-more-information until we've loaded the 33M edges
into a candidate and replayed the check.
