from datetime import datetime

MESSAGE_KINDS = ("Post", "Comment")


def _root_post(G, message_id):
    """The Post a thread starts from. A post starts its own thread; a comment follows
    its single outgoing replyOf edge (child -> parent) until it reaches a post."""
    node = message_id
    while G.nodes[node].get("kind") != "Post":
        parents = [v for _, v, d in G.out_edges(node, data=True) if d.get("rel") == "replyOf"]
        if len(parents) != 1:
            raise ValueError(f"comment {node} has {len(parents)} replyOf edges, expected 1")
        node = parents[0]
    return node


def _author(G, post_id):
    authors = [v for _, v, d in G.out_edges(post_id, data=True) if d.get("rel") == "hasCreator"]
    if len(authors) != 1:
        raise ValueError(f"post {post_id} has {len(authors)} hasCreator edges, expected 1")
    return authors[0]


def latest(G, person_id):
    """The person's ten most recent messages (posts and comments), newest first.

    Returns a list of (message id, id of the post the thread starts from, person id of
    that post's author). A post starts its own thread, so for a post the second item is
    its own id and the third is its creator. Fewer than ten if the person wrote fewer.
    Messages with the same creationDate are ordered by larger message id first.
    """
    if person_id not in G or G.nodes[person_id].get("kind") != "Person":
        raise KeyError(f"no person with id {person_id}")
    messages = [
        u
        for u, _, d in G.in_edges(person_id, data=True)
        if d.get("rel") == "hasCreator" and G.nodes[u].get("kind") in MESSAGE_KINDS
    ]
    # creationDate is ISO datetime text with a zone: compare as instants, not as strings.
    messages.sort(
        key=lambda m: (datetime.fromisoformat(G.nodes[m]["creationDate"]), m),
        reverse=True,
    )
    result = []
    for m in messages[:10]:
        post = _root_post(G, m)
        result.append((m, post, _author(G, post)))
    return result
