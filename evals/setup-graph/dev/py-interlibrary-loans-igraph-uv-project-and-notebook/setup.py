"""Writes data/loans.graphml: a generated loan network (seed 2311), the shape the statistics office exports."""
import random
import sys
from pathlib import Path

work = Path(sys.argv[1])
rng = random.Random(2311)
libs = [f"LIB-{i:02d}" for i in range(1, 31)]
edges = {}
for a in libs:
    for b in rng.sample([x for x in libs if x != a], rng.randint(2, 5)):
        edges[(a, b)] = (rng.randint(3, 400), round(rng.uniform(4.0, 38.0), 2))
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
         '  <key id="loans" for="edge" attr.name="loans" attr.type="int"/>',
         '  <key id="cost" for="edge" attr.name="cost" attr.type="double"/>',
         '  <graph id="loans2025" edgedefault="directed">']
lines += [f'    <node id="{n}"/>' for n in libs]
for (a, b), (loans, cost) in sorted(edges.items()):
    lines.append(f'    <edge source="{a}" target="{b}"><data key="loans">{loans}</data>'
                 f'<data key="cost">{cost}</data></edge>')
lines += ["  </graph>", "</graphml>"]
(work / "data").mkdir(parents=True, exist_ok=True)
(work / "data" / "loans.graphml").write_text("\n".join(lines) + "\n")
