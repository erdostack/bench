connection() was listing every simple path of up to 6 connections between the two members and keeping the
shortest. That's fine inside the partner-programme group (a thin chain of members), but the main graph has a
hundred-odd members with hundreds to thousands of connections each, and the number of paths through them explodes;
that's the "spins forever" pairs. It now does one breadth-first search (nx.shortest_path), which gives a shortest
chain directly, and returns None when that chain is longer than max_steps or there is none (members of the partner
group can't reach the main graph at all). Same return shape; tests pass; every pair I tried returns in milliseconds.
