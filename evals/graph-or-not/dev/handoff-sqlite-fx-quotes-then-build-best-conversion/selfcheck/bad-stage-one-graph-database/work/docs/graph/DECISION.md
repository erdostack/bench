# Routing conversions through other currencies

Decision: graph-database

## Workload facts (from the owner, 2026-11-23)

- Quotes cache: SQLite on every checkout pod, refreshed every 10 s. 160 currencies, about 2,300 quoted pairs, each
  quoted both ways by one to three providers.
- Treasury's rules (signed off by compliance):
  - at most two intermediate currencies, so at most three conversions;
  - pick the route with the best rate for the customer (best provider on each leg);
  - never route through a currency in `restricted_currency`, even when it would be cheaper.
- About 300 conversions a second at peak; checkout gives this 15 ms.

## Options considered

- graph-database (Arjun's proposal): rejected. A server per pod, or a network hop inside 15 ms, for a graph of a few
  thousand edges that is replaced every 10 s.
- recursive-sql: workable (three steps on the local cache), but the best-rate search is easier to get right in code.
- in-process-library: chosen. Read the best rate per pair into memory when the cache refreshes; search routes of
  at most three conversions, skipping restricted currencies.
- no-graph: no; routing through intermediates is a search.

## What would change the decision

- Treasury allowing more than three conversions (then a shortest path on -log rate, not enumeration).
- Quotes that change faster than the search can be rebuilt.
