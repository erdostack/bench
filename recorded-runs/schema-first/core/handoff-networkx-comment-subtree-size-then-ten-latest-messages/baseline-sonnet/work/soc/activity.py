"""Recent activity for the member panel."""

# The dump's schema is not documented in this repo. These names follow the
# `kind` / `rel` conventions already used by removal.py (kind "Comment",
# rel "replyOf") and the LDBC social-network naming for the rest. Check them
# against a real dump; they are the only places that need changing.
CREATOR_REL = "hasCreator"      # edge: message -> person who wrote it
REPLY_REL = "replyOf"           # edge: reply -> message it answers
DATE_ATTR = "creationDate"      # node attribute on posts and comments
MESSAGE_KINDS = ("Post", "Comment")


def _creator(G, message_id):
    for _, person, data in G.out_edges(message_id, data=True):
        if data.get("rel") == CREATOR_REL:
            return person
    raise ValueError(f"message {message_id!r} has no {CREATOR_REL} edge")


def _thread_post(G, message_id):
    """The post that starts the thread message_id belongs to (a post is its own)."""
    node = message_id
    seen = {node}
    while G.nodes[node].get("kind") != "Post":
        parents = [t for _, t, d in G.out_edges(node, data=True) if d.get("rel") == REPLY_REL]
        if len(parents) != 1:
            raise ValueError(f"comment {node!r} has {len(parents)} {REPLY_REL} edges, expected 1")
        node = parents[0]
        if node in seen:
            raise ValueError(f"{REPLY_REL} loop at {node!r}")
        seen.add(node)
    return node


def latest(G, person_id):
    """Ten most recent messages (posts and comments) written by person_id.

    Returns a list of (message id, id of the post its thread starts from,
    person id of that post's author), newest first; a post's thread post is
    itself. Messages with equal dates are ordered by larger id first so the
    result is stable. Fewer than ten are returned if the person wrote fewer.
    Raises ValueError if person_id is not a person in G.
    """
    if person_id not in G or G.nodes[person_id].get("kind") != "Person":
        raise ValueError(f"no person with id {person_id!r}")
    messages = [
        m
        for m, _, data in G.in_edges(person_id, data=True)
        if data.get("rel") == CREATOR_REL and G.nodes[m].get("kind") in MESSAGE_KINDS
    ]
    messages.sort(key=lambda m: (G.nodes[m][DATE_ATTR], m), reverse=True)
    result = []
    for m in messages[:10]:
        post = _thread_post(G, m)
        result.append((m, post, _creator(G, post)))
    return result
