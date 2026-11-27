I added `latest(G, person_id)` in `soc/activity.py`. It is untested against a real dump, and it relies on three guesses about the dump's layout.

It returns up to ten `(message id, thread post id, thread post author id)` tuples, newest first. A post is its own thread post. If two messages share a date, the one with the larger id comes first. It raises `ValueError` if `person_id` isn't a person in G, if a comment doesn't have exactly one reply link, or if a post has no creator edge.

The repo doesn't document the dump, so I couldn't check the field names. They are constants at the top of the file:
- **Author link:** an edge with `rel == "hasCreator"`, running from the message to the person.
- **Date field:** a node attribute `creationDate` on posts and comments. Sorting needs it to be ISO strings or numbers. Posts and comments need the same type.
- **Node kinds:** `"Post"`, `"Comment"` and `"Person"`. Only `"Comment"` is confirmed, from `removal.py`.

`replyOf` and `kind` are confirmed from `removal.py`. The rest follow the LDBC social-network naming. Please check them against a real dump, or tell me the actual names.

I tested it on a small made-up graph. It had a long reply chain and a post written by another person, and the output was ordered correctly. That doesn't show the real dump has the same layout. Once the file is on the server, a quick `latest(G, <some id>)` in the console will confirm it.
