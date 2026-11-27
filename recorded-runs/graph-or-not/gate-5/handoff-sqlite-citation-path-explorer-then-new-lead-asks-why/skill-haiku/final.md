Decision: graph-database

We decided to move the citation-path explorer to a graph database, but only after two cheaper options have been tried on a copy of the snapshot. The call is provisional until those trials run.

Why, with the numbers it rests on:

- The requirement is chains of up to 6 citations between two papers, skipping retracted papers, at 3 s p95 for 400 staff, over 410M citations and 96M papers (stated in the request).
- The recursive query on the SQLite snapshot runs at 41 s p95 on a copy, which is 13.7 times the 3 s budget (41 / 3). That is measured failing. The query carries the full path as a string, uses UNION ALL so every route is a row, and walks to 6 hops before ranking, so it does much more work than a shortest-path search needs.
- The in-memory options do not fit as they are deployed. Six workers at 6 GB each is 36 GB on a 32 GB host (6 x 6). A networkx copy is about 53 GB per worker (130 bytes per citation x 410M).
- Staying on SQLite is not ruled out, and this is the point you raised. The first trial is a rewrite of the query: visited set in place of the path string, meet in the middle at 3 hops, year and retraction filters applied during the walk. If it meets 3 s p95 on a replay of real searches, the decision is withdrawn and SQLite stays. Nobody has run it yet, so the 41 s figure is what we have.
- The second trial is one memory-mapped copy of Wen's array, shared by the six workers on a 32 GB host. His array takes 6 GB and runs in 0.8 s. The platform team refused the daily rebuild (40 minutes), and the year and retraction filters are about two weeks of work each. If a shared copy meets 0.8 s and the rebuild fits the refresh window, the in-process option would hold.
- If neither passes, the full edge set goes into the candidate graph database, and we run the real search mix with 1.2M new citations a day (about 13.9 a second).

Unknown and not measured yet: the search rate across the 400 staff, the reach of hub papers (a random-graph estimate of about 8.5 neighbours per paper gives roughly 388,000 papers within 6 hops, but real citation graphs have hubs, so the true reach is larger), whether Wen's 0.8 s includes the year and retraction filters, and whether the six workers are processes or threads.

Nothing in the repository was changed.
