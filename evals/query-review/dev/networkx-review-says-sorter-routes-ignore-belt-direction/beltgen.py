"""Generate the conveyor network: induction points feed a main loop that runs one way round, diverters branch off
to chute spurs (one way, ending at a chute), a few return belts and cross-overs, some reversible belts."""
import random


def network(seed=8181):
    rng = random.Random(seed)
    segs = []

    def belt(a, b, m, rev=False):
        segs.append({"id": f"B{len(segs) + 1:04d}", "from": a, "to": b, "metres": m, "reversible": rev})

    loop = [f"L{i:03d}" for i in range(120)]
    for a, b in zip(loop, loop[1:] + loop[:1]):
        belt(a, b, rng.randint(3, 9))
    for k in range(12):
        belt(f"IN-{k:02d}", loop[k * 10], rng.randint(5, 15))
    chute = 0
    for i, node in enumerate(loop):
        if i % 2 == 1:
            spur = [f"D{i:03d}-{j}" for j in range(rng.randint(1, 3))]
            prev = node
            for s in spur:
                belt(prev, s, rng.randint(2, 6))
                prev = s
            belt(prev, f"CH-{chute:03d}", rng.randint(1, 3))
            chute += 1
            if rng.random() < 0.25:                     # recirculation belt back onto the loop further on
                belt(spur[-1], loop[(i + rng.randint(3, 20)) % 120], rng.randint(4, 12))
    for _ in range(10):                                 # cross-overs: short cuts across the loop, one way
        a, b = rng.sample(range(120), 2)
        belt(loop[a], loop[b], rng.randint(8, 20))
    for _ in range(6):                                  # reversible links between neighbouring spurs
        i = rng.randrange(1, 117, 2)
        belt(f"D{i:03d}-0", f"D{i + 2:03d}-0", rng.randint(2, 4), True)
    return {"segments": segs}
