#!/usr/bin/env python3
"""Build graphs/practice/social.json: made-up people for the friend-suggestion training, generated from a fixed
seed (the same graph every time). Anything changed in the practice graph since is gone afterwards."""
import json
import random
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent.parent
rng = random.Random(2468)
FIRST = ["Agnes", "Bertil", "Carys", "Dmitri", "Edda", "Florin", "Greta", "Henrik", "Iris", "Jonah", "Kaia", "Leopold",
         "Mira", "Nanna", "Otto", "Petra", "Rasmus", "Saga", "Teodor", "Una", "Viggo", "Wanda"]
LAST = ["Achterberg", "Bramwell", "Castellan", "Dovey", "Eskildsen", "Fairlie", "Gunnarsson", "Holloway", "Ibbotson",
        "Juhl", "Kavanagh", "Lomax", "Midgley", "Nordqvist", "Oakes", "Pemberton", "Quist", "Rowntree"]
CITIES = ["Brackenford", "Ellerby", "Hollin Cross", "Marrick", "Thornsett"]
TAGS = ["cycling", "baking", "chess", "film", "gardening", "jazz", "running", "sketching", "climbing", "board-games"]
G = nx.DiGraph()
for c in CITIES:
    G.add_node(f"city:{c.lower().replace(' ', '-')}", kind="city", name=c)
for t in TAGS:
    G.add_node(f"tag:{t}", kind="tag", name=t)
names, people = set(), []
while len(people) < 150:
    first, last = rng.choice(FIRST), rng.choice(LAST)
    if (first, last) in names:
        continue
    names.add((first, last))
    pid = f"P{1001 + len(people) * 3 + rng.randint(0, 2)}"
    people.append(pid)
    G.add_node(pid, kind="person", firstName=first, lastName=last,
               creationDate=f"2025-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}T{rng.randint(0, 23):02d}:00:00Z")
    G.add_edge(pid, f"city:{rng.choice(CITIES).lower().replace(' ', '-')}", kind="isLocatedIn")
    for t in rng.sample(TAGS, rng.randint(1, 3)):
        G.add_edge(pid, f"tag:{t}", kind="hasInterest")
while sum(1 for _u, _v, d in G.edges(data=True) if d["kind"] == "knows") < 520:
    a, b = rng.sample(people, 2)
    if G.has_edge(a, b) or G.has_edge(b, a):
        continue
    G.add_edge(a, b, kind="knows", creationDate=f"2026-{rng.randint(1, 10):02d}-{rng.randint(1, 28):02d}T12:00:00Z")
out = ROOT / "graphs" / "practice" / "social.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1, sort_keys=True))
print(f"practice built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
