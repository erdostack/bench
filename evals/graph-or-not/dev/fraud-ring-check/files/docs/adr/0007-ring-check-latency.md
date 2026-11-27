# ADR 0007: ring check latency

**Status:** open, no option chosen · **Last updated:** 2026-10-30

## Context

The ring check has to answer inside the gateway's 250 ms. We give the query a 400 ms statement
timeout so a slow one cannot pile up connections; a cancelled check counts as "no verdict".

## What has been done so far

| When | Change | Result |
|---|---|---|
| 2025-11 | Added `links_entity_account_idx` so both join directions are index-only | 3-step mean went from 590 ms to about 210 ms |
| 2025-12 | `work_mem` raised from 16 MB to 256 MB for the service role | no measurable change |
| 2026-02 | Degree cap: skip entities shared by more than 500 accounts | cancelled checks fell from 11% to about 4% |
| 2026-04 | Synchronous depth lowered from 6 to 4; the 6-step query moved to the review queue | authorisation path stopped exhausting connections |
| 2026-05 | Read replicas 2 → 4 | throughput doubled, per-query latency unchanged |
| 2026-07 | Precomputed two-step table (migrations 0038, dropped in 0042) | abandoned |
| 2026-08 | Group label kept current by the event consumer: every account carries the id of the connected group it belongs to, so the check is one lookup | abandoned after two weeks in shadow mode: 63% of active accounts ended up in a single group even with the degree cap, so the label flagged most payments |
| 2026-09 | Search from both ends in application code | 30 to 200 queries per check, p50 worse than the single query; reverted |

## Proposed and not done

- Nightly precompute of connected groups in the warehouse. The risk team's objection is recorded in
  RISK-881.
- Lower the degree cap below 500. Risk measured the effect on recall: at a cap of 100, 22% of the rings
  confirmed last quarter would not have been found.
