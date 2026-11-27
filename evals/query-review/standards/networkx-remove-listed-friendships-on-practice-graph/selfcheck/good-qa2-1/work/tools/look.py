from collections import Counter
def run(G):
    c = Counter()
    for _u, _v, d in G.edges(data=True):
        c.update([d["kind"]])
    return dict(c)
