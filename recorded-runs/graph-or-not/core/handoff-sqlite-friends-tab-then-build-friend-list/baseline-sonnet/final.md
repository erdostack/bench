I wrote `queries/friends.sql`. It takes `:person_id` and returns one row per friend with `friend_id` and `since`, in that order. `since` is the friendship's `creation_date` as stored, with no conversion. Rows are newest first, and ties are broken by `friend_id` so the order is stable.

It leaves out friends whose account is `closed`, the same as the existing `friends_tab.sql`. The schema only says to see the rows in `account_state`, and there `closed` is code 2. Suspended and pending-verification accounts still show. I assumed "the friends the tab should list" means this closed-account rule still applies. If the tab should list closed accounts, delete the `account_state` join and the `WHERE` line.

I ran it through `sql.run` on the sample `var/hearth.db` for the member with the most friends. Its rows match the old `friends_tab` query's rows, so the output is the same set.

I did not change `hearth/profile.py`, which still calls `friends_tab`.
