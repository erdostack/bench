"""Remove eight friendships (knows edges) from the practice graph, for the suggestion-tool training.

Each pair is stored once, in whichever direction the request was sent, so both directions are checked.
Person ids were resolved from firstName/lastName in graphs/practice/social.json (each name is unique there).
"""

PAIRS = [
    ("P1237", "P1223"),  # Leopold Ibbotson, Edda Eskildsen
    ("P1211", "P1330"),  # Dmitri Dovey, Mira Eskildsen
    ("P1031", "P1030"),  # Jonah Holloway, Henrik Midgley
    ("P1431", "P1416"),  # Bertil Ibbotson, Mira Kavanagh
    ("P1229", "P1318"),  # Mira Bramwell, Edda Achterberg
    ("P1052", "P1305"),  # Saga Bramwell, Kaia Ibbotson
    ("P1066", "P1152"),  # Iris Juhl, Otto Lomax
    ("P1107", "P1008"),  # Greta Midgley, Rasmus Lomax
]


def run(G):
    removed = 0
    for a, b in PAIRS:
        for u, v in ((a, b), (b, a)):
            if G.has_edge(u, v) and G.edges[u, v].get("kind") == "knows":
                G.remove_edge(u, v)
                removed += 1
    return removed
