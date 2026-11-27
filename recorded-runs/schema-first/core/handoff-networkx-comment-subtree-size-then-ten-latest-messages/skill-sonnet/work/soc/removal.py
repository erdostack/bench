import networkx as nx


def removal_count(G, comment_id):
    """Messages deleted if the comment and every reply below it, at any depth, were removed.

    replyOf edges point from a reply to the message it answers, so the replies
    below a comment are its ancestors in the replyOf edges. The comment itself is counted.
    """
    if comment_id not in G or G.nodes[comment_id].get("kind") != "Comment":
        raise KeyError(f"no comment with id {comment_id}")
    replies = nx.DiGraph(
        (u, v) for u, v, d in G.edges(data=True) if d.get("rel") == "replyOf"
    )
    replies.add_node(comment_id)
    return 1 + len(nx.ancestors(replies, comment_id))
