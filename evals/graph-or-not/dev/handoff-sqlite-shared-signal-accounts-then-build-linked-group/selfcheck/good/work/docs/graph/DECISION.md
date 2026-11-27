# Linked-accounts panel

Decision: in-process-library

## Workload facts (from the conversation of 2026-11-24)

- **Linking rule (trust and safety, Ayla): a shared device id or a shared payment card links two accounts. A shared
  IP never does**, not even together with something else (campus wifi, libraries, carriers).
- The current walk (moderation/links.py) stops at max_depth 3: it misses accounts in 31 of 400 groups.
- 240k accounts, 1.1M signal rows; about 200 lookups a day; under 2 s is fine. networkx is installed.

## Options considered

- graph-database (Bilal): rejected, a second store for 200 lookups a day.
- in-process-library: chosen. networkx connected component over device and card links.
- recursive-sql: also fine on the SQLite copy (UNION on account id, device and card only).

## What would change the decision

- Lookups in the sign-up path at high rates, or a rule that weighs signals instead of linking on them.
