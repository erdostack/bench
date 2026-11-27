"""Removal helpers for the moderation console."""


def removal_count(G, comment_id):
    """Messages deleted if this comment and every reply below it, at any depth, are removed."""
    if comment_id not in G or G.nodes[comment_id].get("kind") != "Comment":
        raise ValueError(f"no comment with id {comment_id}")
    # replyOf runs from a reply to the message it answers, so walk the edges
    # backwards from the comment to find everything that sits below it.
    seen = {comment_id}
    stack = [comment_id]
    while stack:
        node = stack.pop()
        for source, _, data in G.in_edges(node, data=True):
            if data.get("rel") == "replyOf" and source not in seen:
                seen.add(source)
                stack.append(source)
    return len(seen)
