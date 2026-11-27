I added `removal_count(G, comment_id)` in `soc/removal.py`. It returns how many messages would be deleted if the comment and every reply below it were removed, at any depth. The comment itself counts as one.

- `G` is the graph from `soc.store.load()`, and `comment_id` is the comment's node id.
- It walks the `replyOf` edges backwards from the comment. Each comment has exactly one `replyOf` edge and the reply graph has no cycles, so nothing is counted twice.
- It raises `ValueError` if the id is not in the dump, or if it belongs to a post. The console can catch that and show no count.

I checked it against `data/threads.json`: for all 1,100 comments it matches an independent count of each comment's descendants. The largest removal in the dump is comment 975912, at 14 messages. I did not wire it into the console, since the request was for the helper function.
