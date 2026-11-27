I'd keep the `list()`. `nx.isolates(G)` is a lazy generator over G's own degree view, so passing it straight to
`G.remove_nodes_from` deletes nodes from G while the generator is still iterating over it, and networkx fails
with `RuntimeError: dictionary changed size during iteration` (the networkx docs for isolates show
`G.remove_nodes_from(list(nx.isolates(G)))` for exactly this reason). I tried it on data/network.json and it
crashes on the first night. The unit test doesn't catch it because its graph has no isolates left by step 3.
The list only holds the isolates, a few hundred names, so there's nothing to save.
