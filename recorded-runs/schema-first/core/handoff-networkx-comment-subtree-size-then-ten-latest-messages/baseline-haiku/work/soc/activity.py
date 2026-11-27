"""Recent activity for the member panel."""

DATE_ATTR = "creationDate"
AUTHOR_REL = "hasCreator"
REPLY_REL = "replyOf"


def _author_of(G, message_id):
    for _, person, data in G.out_edges(message_id, data=True):
        if data.get("rel") == AUTHOR_REL:
            return person
    return None


def _thread_root(G, message_id):
    """Walk replyOf edges up to the post that starts the thread."""
    current = message_id
    seen = {current}
    while G.nodes[current].get("kind") != "Post":
        parents = [
            parent
            for _, parent, data in G.out_edges(current, data=True)
            if data.get("rel") == REPLY_REL
        ]
        if len(parents) != 1 or parents[0] in seen:
            raise ValueError(f"message {current!r} has no single parent in its thread")
        current = parents[0]
        seen.add(current)
    return current


def latest(G, person_id, limit=10):
    """The person's most recent messages (posts and comments), newest first.

    Returns a list of (message id, id of the post the thread starts from, author id) tuples.
    A post starts its own thread, so for a post the first id is also the second.
    """
    if person_id not in G:
        raise ValueError(f"no person with id {person_id!r}")

    authored = [
        message
        for message, _, data in G.in_edges(person_id, data=True)
        if data.get("rel") == AUTHOR_REL
    ]
    for message in authored:
        if DATE_ATTR not in G.nodes[message]:
            raise KeyError(f"message {message!r} has no {DATE_ATTR!r} attribute")

    # Newest first; ties broken by larger id so the order is stable.
    authored.sort(key=lambda m: (G.nodes[m][DATE_ATTR], m), reverse=True)

    result = []
    for message in authored[:limit]:
        root = _thread_root(G, message)
        result.append((message, root, _author_of(G, root)))
    return result
