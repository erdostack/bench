Decision: in-process-library. Written up in docs/graph/DECISION.md.

Grouping is connected components over records linked by a shared email or phone. networkx already did it on the
real export (640k records) in about 2 s and 560 MB, inside a nightly job with a 2 hour window. The current loop is
the bug: it never merges two groups when a later record links them (480,581 groups against 464,663), and it links
on address, which product ruled out. A graph database would be a server for one nightly batch.
