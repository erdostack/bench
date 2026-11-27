Added drainage/upstream.py: a recursive query over pipe from ds_node to us_node, everything that drains into the
node including what pumping stations lift into it. UNION on the node id alone, so the Eastgate loops end.
