I added `sql/friends_2718.sql`. It returns person 2718's friends as friend id, first name, last name and the date the friendship started. Run against `data/circle.db`, it returns 4 friends: Gunnar Jernberg (2018-05-22), Nanna Carlqvist (2019-08-20), Bodil Carlqvist (2023-12-17) and Bodil Ohlin (2024-11-22).

- **Friendship direction:** `knows` stores each friendship once, with the lower id in `person1Id`. The query therefore matches person 2718 in either column and takes the other one as the friend. Filtering on `person1Id` alone would have missed some of them.
- **Date:** it comes from `knows.creationDate`, which is ISO text (YYYY-MM-DD) and the day the friendship was accepted.
- **Schema snapshot:** `docs/graph/schema.md` is new, taken from the live `data/circle.db` on 2026-11-26. I used `--no-samples` because the rows are members' personal data and the snapshot will be committed. `schema.py check` reports 0 findings on the new file.
