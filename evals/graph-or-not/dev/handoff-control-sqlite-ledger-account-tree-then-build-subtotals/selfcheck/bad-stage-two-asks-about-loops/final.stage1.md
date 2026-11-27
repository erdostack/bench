Decision: recursive-sql

1,900 accounts at most 8 deep is a small tree, and the triggers in db/schema.sql guarantee it stays a tree. One
recursive query for each account's descendants, joined to the period's postings (about 260k) and summed, runs well
under the 5 seconds the accountants accept. Tariq's graph database would be a second store for a tree that fits in a
spreadsheet. Written up in docs/graph/DECISION.md.
