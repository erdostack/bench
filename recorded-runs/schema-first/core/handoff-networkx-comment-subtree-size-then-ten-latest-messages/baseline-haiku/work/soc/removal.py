"""Removal helpers for the moderation console."""


def removal_count(G, comment_id):
    """Number of messages deleted if this comment and every reply below it were removed.

    The comment itself counts as one. Replies are the comments whose `replyOf` edge points at
    a message in the thread; each comment has exactly one such edge, so walking the edges
    backwards from the comment visits every reply at any depth once.
    """
    if comment_id not in G:
        raise ValueError(f"no message with id {comment_id!r}")
    if G.nodes[comment_id].get("kind") != "Comment":
        raise ValueError(f"message {comment_id!r} is not a comment")

    count = 1
    seen = {comment_id}
    stack = [comment_id]
    while stack:
        current = stack.pop()
        for reply, _, data in G.in_edges(current, data=True):
            if data.get("rel") == "replyOf" and reply not in seen:
                seen.add(reply)
                count += 1
                stack.append(reply)
    return count
