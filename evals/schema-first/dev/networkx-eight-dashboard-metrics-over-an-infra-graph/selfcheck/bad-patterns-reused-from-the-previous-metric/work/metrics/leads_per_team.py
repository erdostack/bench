def compute(G):
    out = {}
    for person, team, data in G.edges(data=True):
        if data.get("rel") == "member_of" and G.nodes[person].get("role") == "lead":
            name = G.nodes[team]["name"]
            out[name] = out.get(name, 0) + 1
    return out
