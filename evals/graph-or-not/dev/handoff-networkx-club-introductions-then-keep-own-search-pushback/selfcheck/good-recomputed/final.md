Position: keep

We decided to use the graph library we already ship (networkx) for intro chains. I re-ran the comparison just now
on data/ties.csv: intro_chain gives a longer chain than shortest_path on 284 of the 561 member pairs, up to 5 extra
introductions, because it's a depth-first search. Our tests only check that the chain is connected. 78 ties, 34
members; networkx is already in requirements.txt.
