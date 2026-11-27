"""Build the access graph from the identity provider's export.

Edges point from the thing that is given access to the thing it is given: identity -> group (member of),
group -> group (nested in), group -> system (granted)."""
import json
from pathlib import Path

import networkx as nx


def _rows(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load(export_dir):
    export = Path(export_dir)
    g = nx.DiGraph()
    for row in _rows(export / "identities.jsonl"):
        g.add_node(("identity", row["id"]), name=row["name"])
    for row in _rows(export / "memberships.jsonl"):        # {"member": ["identity"|"group", id], "group": id}
        g.add_edge(tuple(row["member"]), ("group", row["group"]))
    for row in _rows(export / "grants.jsonl"):             # {"group": id, "system": "payroll", "level": "admin"}
        g.add_edge(("group", row["group"]), ("system", row["system"]), level=row["level"])
    return g
