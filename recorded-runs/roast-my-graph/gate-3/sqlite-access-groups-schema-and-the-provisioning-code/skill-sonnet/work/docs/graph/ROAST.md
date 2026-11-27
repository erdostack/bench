# Review: accessdb (sql/schema.sql, app/)

Verdict: Not safe as written, and critical. The schema relies on `ON DELETE CASCADE` to remove a deleted group's memberships, nestings and grants, but `app/db.py` never switches foreign keys on, and SQLite leaves them off by default, so the cascade has never run. In `access.db`, 95 rows point at groups that no longer exist, and 62 of 500 users currently get access (87 grants in total, for example `doc/budgets` write and `doc/contracts` write) only through those deleted groups. Separately, because the sync deletes before it creates and ids are reused, a newly created group can take over a deleted group's memberships and grants.

Judged against:
- Engine: SQLite, Python 3.12 (README.md). The sample `access.db` was read on SQLite 3.53.1.
- Model: users belong to groups (`member`); groups nest (`nests`, child to parent); groups hold grants on resources (`access_grant`). A user can open a resource if any group they are in, directly or through nesting, holds a grant on it (`effective_grants` in app/groups.py) (README.md).
- Writers: groups are created and deleted all day by the sync from the HR system (`app/sync.py`). Removing a group must remove its memberships, nestings and grants with it; the schema does that with ON DELETE CASCADE (README.md).
- Connections: every part of the app gets its connection from `app/db.py` (README.md).
- Purpose and urgency: decides who can open what in the document portal; audit next quarter (request).
- Sample size: 500 users, 56 groups, 1,055 memberships, 30 nestings, 61 grants (`access.db`). Production size and sync frequency: not stated.

## Findings

### critical: `connect`
Problem: `connect` in `app/db.py` never runs `PRAGMA foreign_keys = ON`, and SQLite leaves foreign keys off on every new connection, so the `ON DELETE CASCADE` clauses in `sql/schema.sql` never fire. When `delete_group` (called by `sync` for every group HR drops) runs `DELETE FROM grp WHERE id = ?`, the group's rows in `member`, `nests` and `access_grant` stay. `PRAGMA foreign_key_check` on `access.db` returns 95 violations: 89 `member` rows, 2 `nests` rows and 4 `access_grant` rows refer to the four deleted groups 7, 19, 33 and 41. `effective_grants` joins on those ids without checking that the group exists, so the orphans still grant access. Groups 33 and 7 are still nested under the live groups 56 and 57, so their former members inherit those groups' grants. Result on the shipped data: 62 users get 87 entries they should not have: `doc/roadmap` read (22 users), `doc/vendors` read (24), `doc/handbook` read (14), `doc/budgets` write (18) and `doc/contracts` write (9). The README states the required result (removing a group removes its memberships, nestings and grants), so these are wrong grants.
Fix: Switch foreign keys on for every connection in `app/db.py`:
```python
def connect(path=DB_PATH):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA busy_timeout = 5000")
    return con
```
Then remove the existing orphans in one transaction. Both steps were run on copies of `access.db` and left no `foreign_key_check` rows:
```sql
BEGIN;
DELETE FROM member       WHERE group_id NOT IN (SELECT id FROM grp);
DELETE FROM nests        WHERE child    NOT IN (SELECT id FROM grp)
                            OR parent   NOT IN (SELECT id FROM grp);
DELETE FROM access_grant WHERE group_id NOT IN (SELECT id FROM grp);
COMMIT;
```
After this, check `PRAGMA foreign_key_check;` returns nothing. Any other tool that opens `access.db` directly (outside `app/db.py`) also needs the pragma; none is in the repo. For the audit, note that access granted through the orphans over past periods is not recoverable from the database; compare against HR group history if the auditors ask.

### high: `sync`
Problem: `sync` deletes the groups HR dropped and then creates the new ones, in the same run. `grp.id` is `INTEGER PRIMARY KEY` without `AUTOINCREMENT`, so SQLite gives a new row the highest id plus one, which equals the old id when the deleted group had the highest id. With foreign keys off (see `connect`), the old group's rows are still there, so the new group takes them over. On a copy of `access.db`, `delete_group` on group 60 (the highest id, 30 members, admin on `doc/salaries`) followed by `create_group(con, "new-hire-pilot")` returned id 60, and the 30 former members of the deleted group then held the new group's access: `doc/salaries` admin, `doc/board-minutes` read and the rest. In production this happens whenever HR drops the newest group and adds another in the same run.
Fix: The cause is fixed by `connect` above; with foreign keys on, the delete removes the old group's rows and a reused id inherits nothing (tested on a copy: no rows left for group 60). Optional insurance so ids are never reused: declare `grp.id INTEGER PRIMARY KEY AUTOINCREMENT` (needs a table rebuild: create the new table, copy `id` and `name`, drop the old one, rename).

### low: `sync`
Problem: Question to confirm. `sync` deletes every group in `grp` that is not in `hr_groups`. If the HR feed arrives empty or truncated, all matching groups are deleted, and with foreign keys on, all their memberships and grants go with them. Nothing in the files shows that this happens or that the caller checks the list, so this is hardening.
Fix: Have the caller reject an empty `hr_groups`, or refuse to delete more than an agreed share of groups in one run, and log what it deletes (useful for the audit).

## Holds up
- `effective_grants` (`EFFECTIVE` in app/groups.py): the recursive query uses `UNION` over ids only, so it ends even if the nesting contains a loop (no two-group loop exists in the shipped data). The plan uses primary-key searches for `member`, `nests` and `access_grant`, and takes the highest level per resource, which matches the README. Its one problem is that it trusts rows that cascade should have removed (see `connect`).
- `nests`: `CHECK (child <> parent)` blocks self-nesting; loops between two or more groups are not blocked, but the query tolerates them. Adding a check would be optional hardening.
- `member_group` and `nests_parent`: they index the foreign-key columns that the cascade has to search when a group is deleted. Keep them.
- `access_grant`: the primary key `(group_id, resource)` allows one level per group and resource, and `grant` uses `INSERT OR REPLACE` to change it, which is what the key is for. `level` is constrained to `read`, `write` and `admin`.
- `access_grant.resource`: free text with no resource table. The sample has no spelling variants (no resources differing only by case). It would matter if resources acquire their own properties.
- `add_member`, `nest`: `INSERT OR IGNORE` only skips a repeated pair; it does not skip foreign-key errors, so with the pragma on an unknown user or group id still fails.

## Not checked
- Production data: only the sample copy was available, and names there are replaced.
- Whether anything outside `app/` opens `access.db` without `app/db.py`, and whether other writers delete groups or users.
- There is no function in `app/` that removes a membership, nesting or grant other than deleting the group; whether a revoke path exists elsewhere is not shown in the files.
- How `sync` gets `hr_groups` and how often it runs: not in the repo.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
