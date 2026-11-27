I added `sql/friends_2718.sql`. It lists person 2718's friends with the date each friendship started.

Columns: `friend_id`, `firstName`, `lastName`, `friends_since`. Results are ordered by start date, then id.

The query checks both columns of `knows`, because friendships are stored once with the smaller id in `person1Id`. Against `data/circle.db` (read-only) it returns 4 friends:

| friend_id | firstName | lastName | friends_since |
|---|---|---|---|
| 1293 | Gunnar | Jernberg | 2018-05-22 |
| 9240 | Nanna | Carlqvist | 2019-08-20 |
| 3434 | Bodil | Carlqvist | 2023-12-17 |
| 5507 | Bodil | Ohlin | 2024-11-22 |
