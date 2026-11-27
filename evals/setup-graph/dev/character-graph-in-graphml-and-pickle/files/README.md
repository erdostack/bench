# castgraph

Who holds a novel together? A small study of the character co-occurrence network of *Les Misérables* (Knuth's
classic dataset, as shipped with NetworkX).

The graph is a file, not a service: `data/lesmis.graphml` is the source of truth and `cache/lesmis.pickle` is a
ready-to-load copy that `castgraph.io` rebuilds whenever the GraphML is newer.

    pip install -r requirements.lock
    make analyze
    python -m castgraph.analyze brokers --top 5
