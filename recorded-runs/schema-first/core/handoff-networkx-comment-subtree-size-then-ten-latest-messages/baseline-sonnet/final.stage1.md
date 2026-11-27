I added `removal_count(G, comment_id)` in a new file, `soc/removal.py`. It returns how many messages would be deleted if you removed that comment and every reply below it: the comment itself plus all replies at any depth, including replies to replies.

- **How it counts:** it follows only the `replyOf` edges, which point from a reply to the message it answers. Other relations such as `hasCreator` and `containerOf` are ignored, so authors and forums never inflate the count.
- **Bad ids:** it raises `ValueError` if `comment_id` isn't a comment in the graph. A post, person or forum id is rejected too, so the console can't show a post's thread size as if it were a comment's.

I ran it on every one of the 1,100 comments in `data/threads.json` and compared each result with an independent count made with networkx. All 1,100 matched. Counts range from 1 (a comment with no replies) to 14, and 407 comments have at least one reply. I also confirmed that ids 900 (a forum) and -1 (missing) raise the error.

I haven't hooked it into the moderation console, since that code isn't in this repo.
