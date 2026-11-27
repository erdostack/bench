"""Recent activity for the member panel."""
from datetime import datetime


def _when(G, message):
    # creationDate carries a UTC offset that varies between messages, so compare
    # parsed instants rather than the text.
    return datetime.fromisoformat(G.nodes[message]["creationDate"])


def _thread_root(G, message):
    """The post a message's thread starts from. A post starts its own thread."""
    node = message
    while G.nodes[node].get("kind") == "Comment":
        # replyOf runs from a reply to the message it answers; each comment has one.
        node = next(
            target
            for _, target, data in G.out_edges(node, data=True)
            if data.get("rel") == "replyOf"
        )
    return node


def _author(G, post):
    """The person who created a post (its hasCreator edge)."""
    return next(
        person
        for _, person, data in G.out_edges(post, data=True)
        if data.get("rel") == "hasCreator"
    )


def latest(G, person_id):
    """Ten most recent messages (posts and comments) by a person, newest first.

    Returns (message id, id of the post the thread starts from, person id of that
    post's author) for each message.
    """
    if person_id not in G or G.nodes[person_id].get("kind") != "Person":
        raise ValueError(f"no person with id {person_id}")
    messages = [
        message
        for message, _, data in G.in_edges(person_id, data=True)
        if data.get("rel") == "hasCreator"
        and G.nodes[message].get("kind") in ("Post", "Comment")
    ]
    messages.sort(key=lambda m: (_when(G, m), m), reverse=True)
    result = []
    for message in messages[:10]:
        root = _thread_root(G, message)
        result.append((message, root, _author(G, root)))
    return result
