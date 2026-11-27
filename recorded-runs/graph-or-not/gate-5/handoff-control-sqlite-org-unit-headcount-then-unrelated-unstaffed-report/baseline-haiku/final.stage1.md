Decision: recursive-sql

The rollup is a walk up a unit tree with at most 8 levels, over about 1,900 units and 23,000 people, run monthly plus the odd rerun. That is small work for SQLite, and the existing `unit_parent` index already serves the parent lookups. A recursive query over the unit tree, joined to `assignment`, gives the rolled-up headcount directly.

Why not the others:
- Graph database: it adds a server to run and keep in step with the nightly HR refresh, to answer a question of this size. It would not be faster in any way that matters at a monthly cadence.
- In-process library: the unitbook project is standard library only (Python 3.11+), so adding a graph library breaks that. Loading the tree into memory would also be needless at this size.
- No graph: the rollup does need the hierarchy, so a traversal is required.

Sketch (untested; `var/unitbook.db` is not in the workspace):

    WITH RECURSIVE anc(unit_id, ancestor_id) AS (
      SELECT id, id FROM unit
      UNION
      SELECT a.unit_id, u.parent_id
      FROM anc a JOIN unit u ON u.id = a.ancestor_id
      WHERE u.parent_id IS NOT NULL
    )
    SELECT u.id, u.name, COUNT(DISTINCT x.person_id) AS people_rolled_up
    FROM unit u
    JOIN anc ON anc.ancestor_id = u.id
    LEFT JOIN assignment x ON x.unit_id = anc.unit_id
      AND x.start_date <= :as_of AND (x.end_date IS NULL OR x.end_date >= :as_of)
    GROUP BY u.id, u.name
    ORDER BY u.name;

Points to get right before this goes into the pack:
- Count distinct people, not assignment rows. A person with two current assignments under the same top unit would otherwise be counted twice. The sketch uses `COUNT(DISTINCT x.person_id)`. The existing `reports/assignments_by_unit.sql` counts `a.id`, which counts assignments, not people; it is correct only for direct assignments, and it has the same issue if read as headcount.
- `UNION` (not `UNION ALL`) guards against a cycle in `parent_id`, which the schema does not prevent.
- Decide whether closed units (`closed_on` set) belong in the pack. The sketch includes them.
- Nothing was run. There is no `var/unitbook.db` in the workspace, so the query's results and timing are unverified. At this size it should run in well under a second, but check the totals against a known figure, such as the top unit's headcount against the count of current people in the HR system.
