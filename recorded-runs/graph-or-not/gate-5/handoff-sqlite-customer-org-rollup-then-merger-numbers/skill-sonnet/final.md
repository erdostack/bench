Still stands: yes

The decision in docs/graph/DECISION.md is recursive-sql: keep the recursive queries on the SQLite file. The merger moved the numbers a lot, but neither of the two triggers we agreed with ops has been hit. Those triggers are a nightly rollup past 20 minutes, or the account-page subtree query over 150 ms p95.

The numbers, old against new:
- Organisations: 2,300 before, 9,800 now (about 4.3 times).
- Deepest group: 7 levels before, 12 now.
- Nightly rollup: about 2 min before, 6 min 40 s (400 s) now. The trigger is 20 min, so headroom fell from 10 times to 3 times (1,200 s / 400 s).
- Account-page subtree query: 12 ms p95 before, 41 ms p95 now. The trigger is 150 ms, so headroom fell from 12.5 times to about 3.7 times.
- Load: 40 page loads a minute before, 90 now. That is about 1.5 queries a second, and each query is still 41 ms.

Bram is right that everything got worse. The decision only changes when something crosses a trigger, and nothing has. Both queries are still tree walks over a forest (`org.parent_id` is a single column). The depth cap of 30 is far above 12 levels. The rollup time grew about 3.3 times for 4.3 times the organisations, so it is not growing faster than the data.

Headroom is thinner, so the next merger or a doubling of the data could cross a trigger. Before that, I would keep an eye on the rollup. The first step would be to check whether the time is in the ancestor walk or in the `invoice` join, before moving any data. I did not measure anything myself. There is no copy of `var/orgbook.db` in the repo, so these are your figures.

I did not edit docs/graph/DECISION.md, because the decision stands. It still carries the pre-merger numbers (2,300 organisations, 7 levels, 2 min, 12 ms, 40 a minute). If you want, I can refresh its facts to the post-merger figures and record the new headroom of 3 times and 3.7 times. Nothing else in the repo was changed.
