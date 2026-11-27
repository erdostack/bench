Decision: no-graph

The Friends tab is a one-hop lookup: the member's direct friends, joined to the `person` table and sorted by `creation_date`. It needs no traversal, so there is no reason for a graph database, a graph library, or recursive queries. Keep friendships in the existing SQLite database and serve the tab with an indexed query.

Why:

- A friends list is the set of rows in `person_knows_person` where the member is either `person1_id` or `person2_id`. The primary key covers the first case and `person_knows_person_2` covers the second, so both halves are indexed lookups. Joining to `person` for names and filtering out closed accounts is a simple join at this size.
- The volume is small. Production is about 12,000 members and 160,000 friendships, and the tab opens about 20 times a second at peak. Each open is one indexed lookup returning one member's friend list, which SQLite does in well under the time budget. Nothing about this needs a second store.
- Neo4j would add a second copy of the friendships that has to be kept in step, and it would not make a one-hop list faster. "A friends list is a graph query" is true in the abstract, but the query is one hop deep.
- Recursive SQL is not needed either, since nothing is traversed beyond the first hop.

The legal rule goes in the WHERE clause:

- Exclude a friend whose account is closed. In `account_state`, that is the row with `label = 'closed'` (code 2 in the sample). Filter by the state's label or code through a join, not by hard-coding the number, so a renumbered table does not silently change the rule.
- Keep friends whose account is suspended (code 3) or pending verification (code 4), as the rule says everyone else still shows.
- Order by `creation_date` descending, which is the friendship's start date, to match "newest first". Friendship start is `person_knows_person.creation_date`, not the member's own creation date.

Points to confirm before shipping:

- The rule does not say what happens when the member whose tab is open has closed their own account. Check with legal or with the product owner before the page is served for closed members.
- Both `person1_id` and `person2_id` must be matched, since each friendship is stored once with the smaller id first. A query that checks only one side will miss half the friends.
- Time the query on a copy of production data before shipping. The sample in `var/` has 1,700 friendships, which is too small to show real timings.
