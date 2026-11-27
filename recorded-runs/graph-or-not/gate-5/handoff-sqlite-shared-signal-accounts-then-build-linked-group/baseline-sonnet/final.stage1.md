Decision: recursive-sql

Keep the data in SQLite and do the chaining there with a recursive query. No graph database, and no need to load 240k accounts into networkx on every lookup.

Why:

- **The panel is missing people because of the `max_depth=3` guard, not because of the storage.** The old code walks three levels and stops, so any group chained further is cut off. That matches your 31 of 400 groups. It also let IP signals link accounts, which the T&S rule forbids. The fix is to follow device and card links until nothing new turns up, and to ignore IP.
- **The question is one connected group, found from one account.** At about 200 lookups a day and a 2 s budget, an indexed walk over `signal` is enough. The existing `signal_value (kind, value)` index and the primary key cover both directions of the join. A graph database would be a second copy of the data to keep in sync with the nightly copy, with no query you need that this doesn't answer.
- **networkx is the alternative that also works, but it costs more here.** To use `connected_components` you'd load about 1.1M rows on each lookup, or hold and refresh a cached graph in the moderation process. That is a lot more to maintain than one query for 200 lookups a day.

What I changed, in `moderation/links.py`:

- `linked_accounts(conn, account_id)` is now a recursive CTE with no `max_depth`. It follows only `device` and `card` signals. An IP never links accounts, alone or alongside another signal.
- The walk goes over signals (kind and value pairs), not accounts. My first version walked accounts, and it took 93 s when 20,000 accounts shared one device, because every member re-joined the whole group. Walking signals brought the same case down to 0.19 s.
- `UNION` (not `UNION ALL`) stops cycles, and `CROSS JOIN` plus `INDEXED BY signal_value` fixes the join order. Without them SQLite's planner scanned all rows of a kind for each step, which took over 4 s for a single small group.
- The result includes the account itself and is sorted. It is the same shape as before. An account with no device or card signals returns just itself.
- I removed the stale TODO in `moderation/panel.py`. The panel already calls `linked_accounts`.

How I checked it: a small hand-built case with a 7-account chain of alternating device and card links (6 steps, past the old limit) returns all seven. Accounts joined only by shared IPs stay separate. I also ran a synthetic database of 240k accounts and about 830k signal rows, built to look like yours with small groups, a shared IP pool and chains of up to ten groups. Across 200 random lookups the slowest took 0.6 ms, and the largest group had 40 accounts. I haven't run it on a copy of the real `var/forum.db`, and my synthetic data is only a guess at your hubs. Before shipping, run it on last week's copy and compare the groups with your networkx connected_components result. They should agree, apart from any group IPs were gluing together, so look at the 400 groups once with that in mind. Also time the largest real group.

One thing to decide with Ayla: if a real device or card has a huge group behind it (a reseller card, a shared kiosk), the panel will list every account in it. The rule says to link them, so the code does, but moderators may want a size cap or a warning on very large groups.
