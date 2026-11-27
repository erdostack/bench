Decision: graph-database

Hi Marisol, we decided on a graph database for the path search, recorded in docs/graph/DECISION.md. Short
version of why staying on the SQLite snapshot was ruled out:

- The search is shortest chains up to 6 hops over 410M citations, filtered on retraction and year mid-walk, with a
  3 s p95 budget. The recursive query in sql/path.sql, with indexes both ways, measured 41 s p95.
- Holding it in memory with networkx is about 53 GB per worker; we run 6 workers on 32 GB hosts.
- Wen's numpy array fit, but each filter took about two weeks and a rebuild for the 1.2M new citations a day takes
  40 minutes; platform declined to run it. A closure table came to about 90 billion rows.
