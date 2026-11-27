Still stands: yes

| | when we decided | now |
|---|---|---|
| members | 220k | 610k |
| connections | 3.1M | 9.8M |
| peak profile views | ~90/s | ~240/s |
| mutual-connections query p95 | 7 ms (copy of prod) | 19 ms (prod) |
| line agreed with Lena | 50 ms p95 | 50 ms p95 |
| panel budget | 100 ms | 100 ms |

The data roughly tripled and the query went from 7 ms to 19 ms. That is still well under the 50 ms line you and Lena
agreed would trigger a proper look at a graph database, and under a fifth of the panel's 100 ms. On the terms set
when we decided, nothing has been crossed. Worth keeping an eye on the p95 trend; the record in
docs/graph/DECISION.md already says what to do if it reaches 50 ms.

Capacity is not a worry either: `src/db.ts` caps the pool at 10 connections per container, and at 19 ms a query
that is far more than the peak needs.
