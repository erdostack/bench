# Decision: which option for the links endpoint, the Neo4j cutover (ADR 0009) or PostgreSQL?

Decision: no-graph

No-go. Do not spend the sprint on the loader.

## Workload facts

ADR 0009 was accepted in January, before launch, on the expectation that users would follow chains four
to six steps out and ask how two entities are connected. Production since March says otherwise.

- October, from `ops/api-usage-2026-10.csv` (I added up the daily rows): 2,368,110 link requests, of
  which 2,318,400 asked for one level (97.9%), 47,300 for two (2.0%) and 2,410 for three (0.1%).
- The UI and the API stop at three levels (changelog, 2026-08-12; `app/links.py` rejects more).
- The connection finder, the one feature that needed real path-finding, was removed on 2026-06-17 after
  11 accounts had used it in three months.
- p95 is 14 ms for one level, 85 ms for two and 610 ms for three, over 21.4 million links.
- The primary runs at 9% CPU on average and 18% at peak. The 212 statements over a second in October
  were all wildcard searches, none of them link expansions.

## Options considered

- Finish the loader and cut over to Neo4j (the ADR): rejected. It would add a datastore, a nightly sync
  and a drift check to serve what is, 98 times in 100, a single indexed lookup that already answers in
  14 ms. The premise it was accepted on did not come true.
- Keep `links` in PostgreSQL with the query the endpoint has now: chosen. The occasional two- and
  three-level expansion is covered by the same depth-limited query.
- Loading 21.4 million links into each API process: no reason to.

## What would change the decision

- Product bringing back path-finding or lifting the three-level cap, with usage to match.
- The three-level request getting slower than users accept as `links` grows: look at that query first.

Suggested follow-up, not done here: mark ADR 0009 as superseded and decide what happens to `graph/`.
