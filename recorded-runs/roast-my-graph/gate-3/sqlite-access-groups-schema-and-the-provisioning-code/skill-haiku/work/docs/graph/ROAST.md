# Roast: accessdb sql/schema.sql and app/

Verdict: Not nothing serious. The README says deleting a group removes its memberships, nestings and grants, and the schema says so too. The code never turns on the foreign keys, so the cascade never runs. access.db already shows the result: 88 user and resource pairs get access through groups HR has deleted. Fix the connection first, then the delete, before the audit.

Judged against:
- README: users belong to groups (member); groups nest (nests, child -> parent); grants sit on resources (access_grant); a user may open a resource if any group they are in, directly or through nesting, holds a grant; removing a group must remove its memberships, nestings and grants, and the schema does that with ON DELETE CASCADE; every part of the app takes its connection from app/db.py (README.md).
- Scale on access.db (a copy of production with names replaced): 500 users, 56 groups, 1,055 memberships, 30 nestings, 61 grants (access.db, read-only).
- Groups are created and deleted all day by the HR sync (app/sync.py).

## Findings

### critical: `connect`
The cascade is written in the schema and switched off in the code. Nothing in between checks.
Problem: connect() does not set PRAGMA foreign_keys, and SQLite leaves it off by default (0 on this connection). The ON DELETE CASCADE clauses never run. access.db already has 89 member rows pointing at deleted groups (7, 19, 33, 41), 2 nests rows and 4 access_grant rows pointing at missing groups. Walking the nesting from those memberships, 88 user and resource pairs get access through deleted groups, and 60 of them have no live path at all.
Fix: Run PRAGMA foreign_keys = ON in connect(), before any other statement. Before the first write, list the orphans with PRAGMA foreign_key_check and review the 88 pairs with the audit team, since removing the orphans removes that access. Then delete the orphan rows in member, nests and access_grant, and check again with foreign_key_check.

### critical: `delete_group`
A deleted group's id can come back, and it brings its old memberships and grants with it.
Problem: delete_group() deletes only the grp row and relies on the cascade, which does not run. The grp id is INTEGER PRIMARY KEY without AUTOINCREMENT, so a deleted id is reused when it was the highest. Tested on a copy: deleting group 60 left its 30 member rows and 3 grants in place, and create_group returned id 60, so the new group inherited all of them. A group HR creates later can open documents that belonged to a deleted group.
Fix: Make delete_group delete explicitly in one transaction: DELETE FROM member WHERE group_id = ?; DELETE FROM nests WHERE child = ? OR parent = ?; DELETE FROM access_grant WHERE group_id = ?; then DELETE FROM grp WHERE id = ?. Rebuild grp as id INTEGER PRIMARY KEY AUTOINCREMENT so a deleted id is never issued again. Checked in memory: after deleting 2 the next id is 3 with AUTOINCREMENT, and 2 without it. Do the rebuild in the same migration as the orphan cleanup.

### low: `sync`
A rename or a partial run changes access with no record.
Problem: sync() calls delete_group and create_group one at a time, and each commits on its own, so a failure partway leaves the groups half-mirrored. A group renamed in HR is deleted and created again under a new id, which drops every grant on the old name. The files do not say whether that is intended.
Fix: Run the whole sync in one transaction. Confirm with the owners whether a rename should carry grants across, and if so, make it an explicit rename.

### low: `DB_PATH`
The database is whatever file is in the current directory.
Problem: DB_PATH is the relative name "access.db", so connect() opens the file in the working directory. Run from elsewhere, it creates an empty database or opens a stale copy, and the grants come from that copy. Nothing checks which file was opened.
Fix: Resolve the path from the project root and fail at startup if the file or its tables are missing.

## Holds up
- `effective_grants`: the recursive walk uses UNION, and since each row carries only the group id, a cycle in nesting still terminates. nests has CHECK (child <> parent), which blocks only the one-step loop.
- The level rule (read, write, admin, taking the highest) matches README, and the CHECK on access_grant.level keeps the values valid.
- Indexes: member is keyed by user_id for the walk, nests by child for the walk, access_grant by group_id for the grant lookup, and member_group covers the group-side lookup needed for deletes.
- `grant`: INSERT OR REPLACE on (group_id, resource) gives one level per group and resource, as intended.

## Not checked
- Nothing was written to access.db or the repo. The orphan counts were read from a read-only connection, and the delete and id-reuse behaviour was tested on a scratch copy that was then removed.
- The HR sync's real calls and frequency were not available, so the rename case is from the code alone.
- The audit scope is not in the repo, so whether the 88 pairs must be reported is for the audit team to decide.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
