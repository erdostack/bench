I added `removal_count(G, comment_id)` to `soc/removal.py`. It returns the comment plus every reply below it at any depth. It raises `KeyError` if the id isn't a comment, including when it's a post id, which makes sense because posts aren't removed through this path.

I compared it with a separate recursive count for all 1100 comments in the current dump, and the two agree. Counts range from 1 to 14.

In the graph, `replyOf` edges point from the reply to the message it answers. The replies below a comment are therefore the ancestors of its node along those edges, not the descendants. Node keys are plain integer ids, so `comment_id` is used as the key directly.

I also took a schema snapshot at `docs/graph/schema.md` from the loaded dump (2026-11-26) and noted the edge direction in a "Verified semantics" section. I used `--no-samples` because the dump holds residents' names.
