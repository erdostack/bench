I added `latest(G, person_id, limit=10)` to `soc/activity.py`. It returns the person's most recent messages (posts and comments), newest first, as tuples of (message id, id of the post the thread starts from, author id of that post). A post is its own thread root.

I could not check it against the real dump because `data/threads.json` is not on this machine. I tested it on a small made-up graph built the same way `store.load()` builds one, and it gave the expected results, including a comment whose thread starts from a post by someone else.

The function assumes four things about the dump that I could not confirm from the repo. Please check these on the console before relying on it:

- Each message node has a `creationDate` attribute. The function raises a KeyError if it is missing.
- Authorship is an edge with `rel` = `hasCreator`, pointing from the message to the person.
- Node `kind` values are `"Post"` and `"Comment"`, as `soc/removal.py` already uses.
- A comment's `replyOf` edge points from the comment to the message it replies to, as `soc/removal.py` implies.

If the person id is not in the graph, the function raises ValueError, matching `removal_count`. A person with no messages gets an empty list.
