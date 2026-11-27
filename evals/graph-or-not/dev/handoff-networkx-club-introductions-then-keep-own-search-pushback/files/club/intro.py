"""Who can introduce me: a chain of members who know each other, from one member to another."""


def intro_chain(ties, a, b):
    """ties: iterable of (member, member) pairs. Returns [a, ..., b] or None."""
    knows = {}
    for x, y in ties:
        knows.setdefault(x, set()).add(y)
        knows.setdefault(y, set()).add(x)
    if a not in knows or b not in knows:
        return None
    stack = [(a, [a])]
    seen = {a}
    while stack:
        member, chain = stack.pop()
        if member == b:
            return chain
        for other in sorted(knows[member], reverse=True):
            if other not in seen:
                seen.add(other)
                stack.append((other, chain + [other]))
    return None
