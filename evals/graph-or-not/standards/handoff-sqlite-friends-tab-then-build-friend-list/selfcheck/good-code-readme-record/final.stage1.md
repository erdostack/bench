Decision: recursive-sql

Stay on SQLite; nothing here actually recurses. The tab is the member's friendships (either column of
person_knows_person) minus friends with a closed account, which legal says are never listed while suspended ones
still show. 160,000 friendships and 20 opens a second is a trivial indexed query. I added a "Decisions" section to
the README so the rule is written down.
