# Friends tab

Decision: recursive-sql

- 12,000 members, 160,000 friendships, about 20 tab opens a second at peak.
- Legal: a friend who has closed their account is never listed; suspended accounts still show.
- Walk the friendship graph with a WITH RECURSIVE query over person_knows_person, depth-limited, on SQLite.
