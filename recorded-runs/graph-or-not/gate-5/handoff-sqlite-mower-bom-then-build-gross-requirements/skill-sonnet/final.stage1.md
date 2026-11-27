Decision: recursive-sql

Stay on Postgres and write this as a recursive query. Gross requirements is "walk down one item's BOM to a depth that depends on the data and sum the bought parts". You already ran that on your biggest ride-on mower and got 0.4 s against a 3 s budget (7.5 times inside it), at about 300 calls a day. Nothing is failing, so there is nothing for a graph database to fix, and it would add a nightly feed from PLM plus a new query language.

The numbers it turns on:
- Size: 48,000 items and 210,000 BOM lines, so about 4.4 components per item, depth up to 11.
- Load: 300 a day is about 0.0035 calls per second.
- Index: bom_line's primary key (parent_id, component_id) already serves a walk down from a parent.

How to build it (I did not change any code): add one WITH RECURSIVE query in sql/ (it has to run on both Postgres and SQLite, and this does). Start at :item_id with need = :qty, join bom_line on parent_id, and multiply need by qty_per x 1.04 at each step. Then sum need per part for items where make_buy = 'B'. Multiplying 1.04 once per level gives the compounding the planning lead wants: a part three levels down gets 1.04^3. I checked the formula on a four-item SQLite test (10 units, answer 118.976, matching the hand sum).

Not found: the exact query behind your 0.4 s, so I can't tell whether it already included the 4% factor (it doesn't change the work). Also missing: the row count it returns, and whether any BOM contains a cycle, which would make the query loop (a depth guard of 12 would cover it). Please re-time it with the scrap factor on the same copy. Only if it measures over 3 s on a full-size copy would an in-memory copy be worth discussing. A graph database would need much heavier or much more frequent use than 300 a day.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
