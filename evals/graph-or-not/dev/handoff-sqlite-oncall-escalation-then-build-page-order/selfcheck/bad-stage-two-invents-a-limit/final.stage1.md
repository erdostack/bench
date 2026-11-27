Decision: recursive-sql

This is a walk of at most five steps over a 2 MB SQLite file, so it stays where it is.

- The SRE leads' rule caps it: at most 4 escalations, so at most 5 policies including the first, and the walk
  stops when it reaches a policy already paged. With 46 loops in the config that second rule is what keeps it
  finite.
- One WITH RECURSIVE query that carries the path and a step count answers it in well under a millisecond on 3,100
  policies, and the page opens about 15 times a minute.
- Neo4j would mean a server next to every pager node and a sync from the admin UI's export, to follow a pointer
  five times. If Malik wants a picture of the whole escalation graph, export it once to a drawing tool.
