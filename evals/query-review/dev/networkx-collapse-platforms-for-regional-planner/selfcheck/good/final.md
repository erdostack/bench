collapse_platforms() builds a new DiGraph (the input is untouched): station nodes with their attributes,
and an edge A->B for every run from a platform of A to a platform of B, keeping the fastest minutes when
several platforms pairs connect the same stations. Transfers, access links and the 40 reversing moves
(runs between two platforms of the same station) are dropped, since at station level they'd be self-loops,
and planner/regional.py's check() rejects those (they'd also inflate "direct trains to N places").

On last night's network: 260 stations, `nx.number_of_selfloops(S)` is 0, and a count of the result's
edges against `count(distinct station pairs with a run)` matches; check() passes.
