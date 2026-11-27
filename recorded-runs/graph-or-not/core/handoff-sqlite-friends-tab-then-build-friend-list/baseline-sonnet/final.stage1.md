Decision: no-graph

The Friends tab is a one-hop lookup, not a graph traversal. It needs the member's direct friends, each friendship's start date, and a sort. That is a plain indexed SQL join in the SQLite database you already have. Neo4j, a graph library and recursive SQL would all add machinery for a query that has no path-finding in it.

Scale: about 12,000 members and 160,000 friendships is about 27 friends per member. At about 20 opens a second this is trivial for SQLite. The existing primary key on (person1_id, person2_id) and the `person_knows_person_2` index on person2_id cover both directions of the lookup, and the query plan shows both are used.

What I added:
- `queries/friends_tab.sql`, in the repo's one-query-per-file style, and `friends_tab()` in `hearth/profile.py`, which calls it. It returns (id, first_name, last_name, friends_since), newest friendship first, with ties broken by member id.
- The legal rule: a friend whose account is closed is never listed. The query joins to `account_state` and filters on the label `closed` (code 2), not on a hard-coded code. Suspended, pending verification and active accounts still show.

Checked on the sample in `var/hearth.db` for the first 200 members: 1,440 friend rows, the counts match an independent query, and every list is in newest-first order.

Two things to know:
- Friendships are stored once with the smaller id first, so the query reads both columns. That is the UNION ALL in the file.
- The list is not paginated. Most members have about 27 friends, but a member with thousands of friends would get all of them in one response. Pagination is worth adding if the product allows that.
