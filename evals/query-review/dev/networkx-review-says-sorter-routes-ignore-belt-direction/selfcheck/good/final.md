The reviewer is right. docs/plant.md says each belt only carries totes from `from` to `to`, but `load_conveyors`
built an undirected graph, so `route()` could use any belt backwards. It only looked fine in testing because most
short routes happen to run with the loop; of 60 random induction-to-chute pairs, 50 got a route that's impossible or
not the shortest real one, and chute-to-induction "routes" were returned although no tote can travel that way.

Changed it to a DiGraph with one edge per belt in its direction, plus the reverse edge for the six belts marked
`reversible` (the docs allow using those both ways). `route()` is unchanged and returns None when the tote can't get
there.
