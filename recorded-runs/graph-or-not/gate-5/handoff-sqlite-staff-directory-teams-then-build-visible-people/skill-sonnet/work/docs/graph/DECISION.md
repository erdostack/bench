# Graph decision

Decision: no-graph

The question: limit staff profiles to colleagues who share a team with the viewer, where a shared team counts only if it has at most 40 current members, and Rhea's proposal to bring in Neo4j. The answer is no graph at all: "do these two people share a qualifying team" crosses the membership link table once (viewer's teams, then the other person's teams), with a size filter. On a synthetic database of the stated size that check took 1.7 ms on average and 12 ms at worst.

## Workload facts

- The question asked of the connections: is there a team that both viewer and subject are currently in, whose current member count is 40 or less. Person to team to person is one hop through team_member, with no repeated walk, no depth parameter and no whole-graph algorithm (db/schema.sql: person, team, team_member; directory/profiles.py TODO and current_teams()).
- 9,200 people, 1,350 teams, 41,000 membership rows, about 6,000 of them ended (left_at set) (stated by the user).
- Current memberships: 41,000 - 6,000 = 35,000, about 3.8 per person (35,000 / 9,200) (derived from stated numbers).
- About 50 profile views a minute on a busy morning (stated by the user): 50 / 60 = 0.83 per second, so a 12 ms worst-case check is about 1% of one core.
- Rule signed off by the DPO (stated by the user): a shared team only counts if it has at most 40 current members, so the company-wide team (8,900 people) and the office-location teams do not make everyone visible to everyone; a membership that has ended does not count, not for who is in the team and not for its size either.
- Everything is in the directory's SQLite database, about 6 MB (stated by the user); the schema keeps one row per stint, a person who rejoins gets a new row (db/schema.sql).
- Indexes exist on team_member(person_id) and team_member(team_id) (db/schema.sql); the query plan used both (measured, EXPLAIN QUERY PLAN, SQLite 3.53.1).
- Team kinds in the schema: team, project, location, company; the size rule is on member count, not on kind, so the rule covers kinds the schema may add later (db/schema.sql, rule as stated by the user).
- Measured on a synthetic in-memory database built from db/schema.sql with the stated sizes (41,000 rows, 6,000 ended, one team of 8,900, location teams, the rest small), 2,000 random viewer/subject pairs: mean 1.7 ms, worst 12.3 ms per check, and about 0.4% of random pairs came out visible. Random data, so it shows the order of magnitude only (measured, Python 3.13 sqlite3, SQLite 3.53.1).
- Writes and freshness: the nightly HR sync and team owners in the UI write to it (README.md); visibility is computed at read time, so a change applies at once. How often owners edit is unknown.
- unknown: the real distribution of team sizes near the cap of 40, and whether a person may always see their own profile; the rule as stated does not say, and the repo has no ticket text. The team-size count has to be recomputed per view or kept in a cached column; which one is for the owner to choose, and the measured time says recomputing is enough.

## Options considered

- graph-database (Neo4j, as Rhea proposes): rejected, because the check is one hop through a link table, not a walk of unknown depth; 6 MB of data and 0.83 views a second are tiny for SQLite, and it would add a second store plus a sync of the memberships that carry a privacy rule.
- in-process-library (the membership edges loaded into memory): rejected, because there is nothing to traverse and a loaded copy would go stale against owner edits, which matters when the rule is about who may see whom.
- recursive-sql (recursive queries on the existing SQLite database): rejected, because nothing recurses: no query follows a relation between things of the same kind more than one step.
- no-graph (plain joins, no traversal): chosen, because the whole rule is a join through team_member with a HAVING count filter, measured at 12 ms worst case at the stated size. Shape of the fix (not applied here): count current members per team with left_at IS NULL, keep teams with at most 40, and allow the profile if the viewer and the subject both have a current row in one such team. Count only current rows for the size, not all rows ever.

## What would change the decision

- A rule that follows relations of unknown length (for example "anyone within two teams of you through people who moved between them", or reporting lines up a hierarchy) would move this to recursive-sql.
- Profile checks measured above the page's budget on the real database, for example the 12 ms worst case turning out an order of magnitude higher, would first mean a plan or index issue, and only then a cached count column; none of that points to a graph engine.
- Membership data growing orders of magnitude beyond 41,000 rows with continuous writes and a rule that needs deep traversal would be the only route to graph-database; nothing in the evidence points there.
