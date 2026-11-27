# why: remove summer fair bays
G.remove_nodes_from([n for n in list(G) if n.startswith('TMP-')])
