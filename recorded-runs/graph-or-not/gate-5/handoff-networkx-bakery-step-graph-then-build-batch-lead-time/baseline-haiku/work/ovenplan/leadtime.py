"""Lead time of a batch: from the first step starting to the last step finishing."""
from collections import defaultdict, deque


def lead_time(conn, recipe_id):
    """Minutes from the first step starting to the last step finishing.

    A step starts as soon as every step it waits on (step_dep) is done. Returns None when the
    recipe has no steps or any of its steps is not timed yet. Raises ValueError on a cycle.
    """
    steps = dict(conn.execute(
        "SELECT id, minutes FROM step WHERE recipe_id = ?", (recipe_id,)).fetchall())
    if not steps or any(minutes is None for minutes in steps.values()):
        return None

    preds = defaultdict(list)
    succs = defaultdict(list)
    waiting = {step_id: 0 for step_id in steps}
    deps = conn.execute(
        "SELECT d.before_id, d.after_id FROM step_dep d "
        "JOIN step b ON b.id = d.before_id JOIN step a ON a.id = d.after_id "
        "WHERE b.recipe_id = ? AND a.recipe_id = ?", (recipe_id, recipe_id)).fetchall()
    for before, after in deps:
        preds[after].append(before)
        succs[before].append(after)
        waiting[after] += 1

    ready = deque(step_id for step_id, count in waiting.items() if count == 0)
    start, finish = {}, {}
    while ready:
        step_id = ready.popleft()
        start[step_id] = max((finish[p] for p in preds[step_id]), default=0)
        finish[step_id] = start[step_id] + steps[step_id]
        for nxt in succs[step_id]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                ready.append(nxt)

    if len(finish) != len(steps):
        raise ValueError(f"step dependencies of recipe {recipe_id} form a cycle")
    return max(finish.values()) - min(start.values())
