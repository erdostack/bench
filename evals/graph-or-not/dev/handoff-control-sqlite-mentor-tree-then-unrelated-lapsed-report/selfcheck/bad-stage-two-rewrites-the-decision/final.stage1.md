Decision: recursive-sql. Written up in docs/graph/DECISION.md.

A mentor's line is a walk down volunteer.mentor_id. With 9,000 volunteers, chains at most 8 deep and about 30
lookups a day, one recursive query on the SQLite file you already have answers it instantly, and it is one more file
in reports/ for the two people maintaining the code. A graph database would be a server on the office machine to run
and keep in sync for 30 lookups a day.
