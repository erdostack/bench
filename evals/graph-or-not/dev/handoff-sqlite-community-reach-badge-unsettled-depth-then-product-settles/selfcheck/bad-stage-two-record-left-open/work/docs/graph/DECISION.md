# "N introductions away" badge

Decision: need-more-information

## Workload facts (from the conversation of 2026-11-24)

- 380k members, 6.4M follow rows, indexed both ways (SQLite).
- Profile views peak at about 70 a second; the badge gets **150 ms** of the page.
- **Open: how far the badge looks.** Dana (growth) wants up to 6 steps, the PM 2 at most; meeting next week.
- Jonas proposes Neo4j.

## Options considered

- 2 steps: a fixed lookup on SQLite (recursive-sql / two joins).
- up to 6 steps: reaches much of the network per view; needs precomputation whatever the store.
- graph-database (Jonas): not justified by anything measured yet.

## What would change the decision

- The depth from the meeting. With 2 steps: stay on SQLite if the lookup fits 150 ms at 70 views a second.
