Added `sql/friends_2718.sql`. It lists person 2718's friends (Ragna Rydell) with the friend's id, first name, last name, and the date the friendship started, ordered by date.

Friendships are stored once in `knows`, with the smaller id in `person1Id`, so the query matches person 2718 in either column. Person 2718 has 4 friends in the live database (`data/circle.db`):

| friendId | firstName | lastName | date |
|---|---|---|---|
| 1293 | Gunnar | Jernberg | 2018-05-22 |
| 9240 | Nanna | Carlqvist | 2019-08-20 |
| 3434 | Bodil | Carlqvist | 2023-12-17 |
| 5507 | Bodil | Ohlin | 2024-11-22 |

The schema snapshot was taken from the database on 2026-11-26 and written to `docs/graph/schema.md`. `schema.py check` reports no findings. I also checked that the friendship date is never before either person's account creation date (0 of 330 rows), which supports the migration's description of it as the acceptance date. That is recorded under Verified semantics.
