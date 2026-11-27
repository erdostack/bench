Decision: no-graph

The DPO rule is a single-hop membership check, not a traversal. A viewer may see a profile when the viewer and the target both have a current membership (left_at IS NULL) in the same team, and that team has at most 40 current members. Nothing is transitive: there is no "friend of a friend" and no path of unknown length. That is a join through one table, which the existing SQLite database does without help. Neo4j would add a second system to keep in sync with the HR sync for no gain in what the rule can express.

The query I tested against the directory schema (db/schema.sql), with the rule applied as written:

    SELECT DISTINCT m2.person_id
    FROM team_member m1
    JOIN team_member m2 ON m2.team_id = m1.team_id AND m2.left_at IS NULL
    JOIN (SELECT team_id, COUNT(*) AS n FROM team_member WHERE left_at IS NULL GROUP BY team_id) s
         ON s.team_id = m1.team_id
    WHERE m1.person_id = ? AND m1.left_at IS NULL AND s.n <= 40

Both places where ended memberships could leak in are covered: the viewer's own membership and the target's membership must be current, and the team size counts only current rows. The company-wide team and location teams over 40 drop out through the size filter.

What I checked, on synthetic rows loaded into an in-memory copy of db/schema.sql (not the real 6 MB database, which I did not have):
- A company team with 50 current members did not make anyone visible through it.
- A viewer whose only team membership had ended saw nobody.
- A person who had left and rejoined a team (two rows, one ended) saw their current teammates only.
- EXPLAIN QUERY PLAN uses team_member_person and team_member_team, so each view touches only the viewer's few rows and their teams. At 50 views a minute the cost is negligible.

Points for the implementation in directory/profiles.py:
- The rule as written does not say whether a person sees their own profile. The query returns the viewer's own id whenever the viewer is in a small team. Decide that explicitly and filter if needed.
- The schema does not stop one person having two open (left_at NULL) rows in the same team. Such a duplicate would be counted twice in the size check and could push a team over 40 early. Check for duplicates in the data and consider a unique partial index on (team_id, person_id) WHERE left_at IS NULL.
- The size subquery aggregates over team_member on each call. That is fine at this volume. If it ever matters, store the current size per team.
- I did not change directory/profiles.py. The TODO is still open.
