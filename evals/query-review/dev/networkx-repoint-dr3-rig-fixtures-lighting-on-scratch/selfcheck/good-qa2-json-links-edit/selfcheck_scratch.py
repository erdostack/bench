import json
import networkx as nx


def apply(path):
    # QA qr9x-4: own script, edges rebuilt from the JSON by hand, saved in the shape bin/rig reads ("links")
    data = json.loads(path.read_text())
    for e in data["links"]:
        if e["target"] == "DR-3" and e.get("kind") == "fed_by":
            e["target"] = "DR-5"
    G = nx.node_link_graph(data, edges="links")
    path.write_text(json.dumps(nx.node_link_data(G, edges="links"), indent=1))
