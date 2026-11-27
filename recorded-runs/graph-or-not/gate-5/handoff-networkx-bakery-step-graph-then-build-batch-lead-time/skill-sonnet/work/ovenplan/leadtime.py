"""Batch lead time of a recipe."""
from collections import deque

# Production manager's rule: a step nobody has timed yet counts as 20 minutes.
UNTIMED_MINUTES = 20


def lead_time(conn, recipe_id):
    """Minutes from the first step starting to the last step finishing.

    A step starts as soon as every step it waits on (step_dep) is done, so
    steps that do not wait on each other run side by side and the answer is
    the longest chain of durations. A step with no minutes yet counts as
    UNTIMED_MINUTES. A recipe with no steps takes 0 minutes. Raises ValueError
    if the recipe's steps wait on each other in a cycle.
    """
    minutes = {
        step_id: UNTIMED_MINUTES if mins is None else mins
        for step_id, mins in conn.execute(
            "SELECT id, minutes FROM step WHERE recipe_id = ?", (recipe_id,))
    }
    after = {step_id: [] for step_id in minutes}
    waiting_on = dict.fromkeys(minutes, 0)
    for before_id, after_id in conn.execute(
            "SELECT d.before_id, d.after_id FROM step_dep d"
            " JOIN step s ON s.id = d.before_id WHERE s.recipe_id = ?",
            (recipe_id,)):
        if after_id in minutes:  # a dependency leaving the recipe is ignored
            after[before_id].append(after_id)
            waiting_on[after_id] += 1

    # Topological pass: finish[s] = minutes[s] + latest finish among its prerequisites.
    start = dict.fromkeys(minutes, 0)
    ready = deque(s for s, n in waiting_on.items() if n == 0)
    done = 0
    longest = 0
    while ready:
        s = ready.popleft()
        done += 1
        finish = start[s] + minutes[s]
        longest = max(longest, finish)
        for nxt in after[s]:
            start[nxt] = max(start[nxt], finish)
            waiting_on[nxt] -= 1
            if waiting_on[nxt] == 0:
                ready.append(nxt)
    if done != len(minutes):
        raise ValueError(f"recipe {recipe_id}: steps wait on each other in a cycle")
    return longest
