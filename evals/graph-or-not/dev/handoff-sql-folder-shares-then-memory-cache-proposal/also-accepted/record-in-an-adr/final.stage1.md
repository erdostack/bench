Decision: recursive-sql. Details are in docs/adr/0007-descendants-of-a-folder-at-share-time.md.

The descendants of a folder are a walk down `folder.parent_id`, which is indexed, and you have already measured it:
12 ms p95 on a replica against a 250 ms budget, on the real 85M rows with trees up to 60 levels. Nothing about that
needs a second system. The alternatives fail on your own constraints. An in-memory tree cannot be held in a 1 GB pod
(85M folders is several GB as Python objects) and, worse, it would be stale: with about 300 moves a second, a share
computed from a copy can grant access to a folder that has just been moved out, which you called a security bug. A
graph database is another copy with the same freshness question plus a system to run.

So: one recursive query inside the share transaction, reading the tree as it is at that moment.
