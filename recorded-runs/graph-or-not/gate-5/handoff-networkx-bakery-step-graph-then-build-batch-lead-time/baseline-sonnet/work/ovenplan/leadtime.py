"""Batch lead time: minutes from the first step starting to the last step finishing."""


class LeadTimeError(ValueError):
    """The recipe's steps cannot be scheduled (untimed step or circular dependency)."""


def lead_time(conn, recipe_id):
    """Length of the schedule of one recipe, in minutes.

    A step starts as soon as every step it waits on (step_dep) is done, so the result
    is the longest chain of dependent steps. Steps that do not depend on each other run
    in parallel. A recipe with no steps has a lead time of 0.

    Raises LeadTimeError, rather than guessing, if any step has no minutes yet (the
    bakers have not timed it) or if the dependencies form a cycle.
    """
    steps = {sid: (name, minutes) for sid, name, minutes in conn.execute(
        "SELECT id, name, minutes FROM step WHERE recipe_id = ?", (recipe_id,))}
    untimed = sorted(name for name, minutes in steps.values() if minutes is None)
    if untimed:
        raise LeadTimeError("steps not timed yet: " + ", ".join(untimed))

    waits_on = {sid: [] for sid in steps}
    for before_id, after_id in conn.execute(
            "SELECT d.before_id, d.after_id FROM step_dep d JOIN step s ON s.id = d.after_id "
            "WHERE s.recipe_id = ?", (recipe_id,)):
        if before_id in steps:
            waits_on[after_id].append(before_id)

    finish = {}

    def finish_of(sid, path=()):
        if sid in finish:
            return finish[sid]
        if sid in path:
            raise LeadTimeError("circular step dependencies in recipe %s" % recipe_id)
        start = max((finish_of(b, path + (sid,)) for b in waits_on[sid]), default=0)
        finish[sid] = start + steps[sid][1]
        return finish[sid]

    return max((finish_of(s) for s in steps), default=0)
