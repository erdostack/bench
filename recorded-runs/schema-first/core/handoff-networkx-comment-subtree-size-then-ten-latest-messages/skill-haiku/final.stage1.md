Added `removal_count(G, comment_id)` to `soc/removal.py`. It returns how many messages would be deleted if the comment and every reply below it, at any depth, were removed. The comment itself is included, so a comment with no replies returns 1.

- `comment_id` is the node id in the dump. It raises `ValueError` if the id is not in the graph or belongs to a post.
- It walks `replyOf` edges backwards from the comment and ignores the other relationship kinds, so people and forums are not counted.

Checked against `soc.store.load()` on the current dump: the result matches a separate walk up each comment's reply chain for all 1100 comments. The largest thread below one comment has 14 messages, and 693 comments have no replies.

The schema snapshot is at `docs/graph/schema.md`. Its Verified semantics section records how the reply direction was settled. The dump has no note on it, so I checked the data: every reply is dated later than the message it answers, once timezone offsets are taken into account.
