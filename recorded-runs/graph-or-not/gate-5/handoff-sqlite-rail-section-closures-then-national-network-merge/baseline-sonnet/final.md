Decision: in-process-library

I wouldn't go with Kofi's suggestion. More cores won't fix this query. A recursive CTE in SQLite runs on one core. Extra cores let more desks run queries at once, but they don't make one cut-off query faster. Your 7.4 s p95 is the latency of a single call.

The indexes aren't the problem either. You confirmed index lookups are in the plan. The cost comes from the query's shape. `sql/cut_off.sql` walks the whole network outward from the core for every closed section. Each call therefore costs the size of the graph (380,000+ sections), not the size of the answer, which is usually a handful of stations. Adding the national network will keep making it slower.

I don't think you need a graph database. The graph is small, it changes once a night and nobody writes to it in between. A server to run and sync would add more than it saves.

My recommendation is to keep the SQLite export and work out the answers once per night. After each export, load the sections into an in-process graph library, or a small routine if you'd rather stay on the stdlib. Find the sections whose closure cuts something off, and store the stations each one cuts off. The desk then looks up the answer instead of traversing the network. Keep `sql/cut_off.sql` as the reference version, and use it to check that the precomputed answers match.

- **Not measured:** I haven't run any of this on your real merged export, so I don't have a number for the new approach. My rough synthetic test on this machine took seconds for a plain Python walk of a graph that size, so loading the graph and walking it on every request isn't a fix. The win is in not walking per request. Please run the precompute on the same test file and compare it with the 7.4 s baseline before switching the desk over.
- **Latency target:** you didn't give one, so I assumed the desk wants answers in about a second or less.
- **When to revisit:** if the desk needs "what if these several sections close together" questions on live edits, answers can't be precomputed per section, and this needs another look. The same goes if the nightly rebuild stops fitting its window.

I couldn't find a place where this was already written down, so I added a "Decision log" section to `README.md` with the decision and these conditions. I didn't change the query or any code.
