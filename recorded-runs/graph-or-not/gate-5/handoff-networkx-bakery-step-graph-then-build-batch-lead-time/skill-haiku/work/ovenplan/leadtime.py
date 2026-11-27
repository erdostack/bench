"""Batch lead time per recipe: the longest path through its steps."""
from collections import defaultdict, deque

# Production manager's rule: an untimed step counts as this many minutes.
UNTIMED_MINUTES = 20


def lead_time(conn, recipe_id):
    """Minutes from the first step starting to the last step finishing.

    A step starts as soon as every step it waits on has finished. Steps
    with no recorded time count as UNTIMED_MINUTES. Returns 0 for a recipe
    with no steps. Raises ValueError on a cycle, or on a dependency that
    links a step of this recipe to a step of another recipe.
    """
    steps = dict(conn.execute(
        "SELECT id, COALESCE(minutes, ?) FROM step WHERE recipe_id = ?",
        (UNTIMED_MINUTES, recipe_id)).fetchall())
    if not steps:
        return 0

    preds = defaultdict(list)
    succs = defaultdict(list)
    deps = conn.execute(
        "SELECT before_id, after_id FROM step_dep "
        "WHERE before_id IN (SELECT id FROM step WHERE recipe_id = ?) "
        "   OR after_id IN (SELECT id FROM step WHERE recipe_id = ?)",
        (recipe_id, recipe_id)).fetchall()
    for before_id, after_id in deps:
        if before_id not in steps or after_id not in steps:
            raise ValueError(f"recipe {recipe_id}: dependency crosses recipes")
        preds[after_id].append(before_id)
        succs[before_id].append(after_id)

    # Kahn's topological order; any step left over sits on a cycle.
    remaining = {s: len(preds[s]) for s in steps}
    queue = deque(s for s, n in remaining.items() if n == 0)
    order = []
    while queue:
        s = queue.popleft()
        order.append(s)
        for t in succs[s]:
            remaining[t] -= 1
            if remaining[t] == 0:
                queue.append(t)
    if len(order) != len(steps):
        raise ValueError(f"recipe {recipe_id}: dependency cycle")

    start, finish = {}, {}
    for s in order:
        start[s] = max((finish[p] for p in preds[s]), default=0)
        finish[s] = start[s] + steps[s]
    return max(finish.values()) - min(start.values())
