"""Generate the fabric: 4 super-spines, 16 spines in 4 planes, 64 racks with a ToR each, 20 servers per rack, each
cabled to its ToR through a patch-panel port (a passive node,
0 ns to the ToR); one rack being recabled (its ToR has no uplinks)."""
import random


def fabric(seed=6060):
    rng = random.Random(seed)
    devices, links = [], []

    def dev(name, kind):
        devices.append({"name": name, "kind": kind})

    def link(a, b, ns):
        links.append({"a": a, "b": b, "latency_ns": ns})

    for s in range(4):
        dev(f"ss{s}", "superspine")
    for p in range(4):
        for s in range(4):
            dev(f"sp{p}{s}", "spine")
            for x in range(4):
                link(f"sp{p}{s}", f"ss{x}", rng.randint(380, 620))
    for row in range(8):
        for r in range(8):
            rack = row * 8 + r
            tor = f"tor{rack:02d}"
            dev(tor, "tor")
            if rack != 37:                                   # rack 37 is being recabled: no uplinks
                plane = rack % 4
                for s in range(4):
                    link(tor, f"sp{plane}{s}", rng.randint(250, 900))
            for k in range(20):
                srv = f"srv{rack:02d}-{k:02d}"
                port = f"pp{rack:02d}-{k:02d}"
                dev(srv, "server")
                dev(port, "patch_port")
                link(srv, port, rng.randint(40, 120))
                link(port, tor, 0)
    return {"devices": devices, "links": links}
