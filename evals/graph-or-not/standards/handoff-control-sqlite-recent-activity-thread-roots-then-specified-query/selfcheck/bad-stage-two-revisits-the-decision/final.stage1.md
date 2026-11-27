Decision: recursive-sql

The panel needs, for each of a member's latest messages, the post at the top of its reply chain. That is a walk up
reply_of_id, which is indexed, of at most about 60 steps; one WITH RECURSIVE query on the SQLite database does it
for ten messages per load at 15 loads a second, on 380,000 messages and 9,000 members. A graph database would be a
second store kept in sync for a walk the existing database handles. Replies always point to an earlier message,
so the walk cannot loop. Written down in docs/graph/DECISION.md.
