"""Remove the eight friendships for the support training (a friendship is stored once, either way)."""
PAIRS = [("Leopold Ibbotson", "Edda Eskildsen"), ("Dmitri Dovey", "Mira Eskildsen"), ("Jonah Holloway", "Henrik Midgley"),
         ("Bertil Ibbotson", "Mira Kavanagh"), ("Mira Bramwell", "Edda Achterberg"), ("Saga Bramwell", "Kaia Ibbotson"),
         ("Iris Juhl", "Otto Lomax"), ("Greta Midgley", "Rasmus Lomax")]


def run(G):
    ids = {f"{d['firstName']} {d['lastName']}": n for n, d in G.nodes(data=True) if d.get("kind") == "person"}
    gone = 0
    for a, b in PAIRS:
        u, v = ids[a], ids[b]
        G.remove_edges_from([(u, v)])
        gone += 1
    return gone
