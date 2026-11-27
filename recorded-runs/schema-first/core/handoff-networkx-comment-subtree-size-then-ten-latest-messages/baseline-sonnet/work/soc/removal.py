def removal_count(G, comment_id):
    """How many messages go if comment_id is removed with every reply below it.

    Counts the comment itself plus all replies at any depth (replies to
    replies included). Only `replyOf` edges are followed; they point from a
    reply to the message it answers. Raises ValueError if comment_id is not a
    comment in G (a post, person or forum id is rejected too).
    """
    if comment_id not in G or G.nodes[comment_id].get("kind") != "Comment":
        raise ValueError(f"no comment with id {comment_id!r}")
    seen = {comment_id}
    stack = [comment_id]
    while stack:
        node = stack.pop()
        for reply, _, data in G.in_edges(node, data=True):
            if data.get("rel") == "replyOf" and reply not in seen:
                seen.add(reply)
                stack.append(reply)
    return len(seen)
