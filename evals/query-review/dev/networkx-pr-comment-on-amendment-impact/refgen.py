"""Generate the framework agreement's cross-references: definitions in clause 1 (which refer to each other),
operative clauses 2 to 30 referring to definitions and to earlier clauses, schedules S1 to S6 referring back."""
import random


def references(seed=1201):
    rng = random.Random(seed)
    defs = [f"1.1({chr(97 + i)})" for i in range(26)] + [f"1.2({chr(97 + i)})" for i in range(14)]
    ops = [f"{c}.{s}" for c in range(2, 31) for s in range(1, rng.randint(3, 9))]
    sched = [f"S{k}.{p}" for k in range(1, 7) for p in range(1, rng.randint(6, 15))]
    refs = set()
    for i, d in enumerate(defs):
        for _ in range(rng.choice([0, 0, 1, 2])):
            refs.add((d, rng.choice(defs)))
    for i, c in enumerate(ops):
        for _ in range(rng.randint(1, 3)):
            refs.add((c, rng.choice(defs)))
        if i and rng.random() < 0.5:
            refs.add((c, rng.choice(ops[max(0, i - 40):i])))
    for s in sched:
        for _ in range(rng.randint(1, 2)):
            refs.add((s, rng.choice(ops)))
        if rng.random() < 0.3:
            refs.add((s, rng.choice(defs)))
    refs = {(a, b) for a, b in refs if a != b}
    return {"references": [{"from": a, "to": b} for a, b in sorted(refs)]}
