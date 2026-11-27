I added `moderation/linked.py` with `linked_accounts(conn, account_id)`. It returns the sorted ids of every account linked to the given one, directly or through a chain of shared signals, and always includes the account itself. `moderation/panel.py` and the first version in `moderation/links.py` are unchanged, since you said you would switch the panel over yourself.

How it differs from the first version: that one stops after `max_depth=3` hops, so it misses longer chains. The new one has no depth cap. It is a recursive query over the `signal` table that tracks account ids with UNION, so a loop in the links terminates. It matches shared signals of any kind (`ip`, `device`, `card`), and it uses the `(kind, value)` index for the joins.

Before you switch the panel, note that the query follows any shared value. A common IP, such as a shared office or mobile carrier address, can join otherwise unrelated accounts, and a chain through it can pull in a large group. If the panel should only follow device or card links, or should weight IP links differently, that is a filter on `signal.kind` in `LINKED_SQL`. I did not add one, because the request did not say.

I checked the function against a small sample in memory: a chain of three accounts through ip, device and card signals, a loop back to the start, a separate pair, a lone account and an unknown id. Results were as expected.
