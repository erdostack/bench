I looked into Dana's comment and I don't think the code should change. Here is what to reply.

`downstream()` has no depth limit, but it is not unbounded. It keeps a `seen` set and skips any node already in it, so every node is queued at most once. On a network with loops the search walks round the ring once, finds everything on it already seen, and stops. The loop body runs at most once per node (about 5,200 here) no matter how the channels are wired.

I checked it against the real network rather than just reading it: `data/network.json` does contain rings (one group of 151 gates that all feed each other through open channels), and calling `downstream()` for every one of the 5,211 nodes takes about half a second in total. For a gate on that ring, `MG-0025`, it returns 2,793 nodes in a couple of milliseconds.

Capping at 10 levels would be a real regression. The main canals run 40 to 70 gates deep; from `MG-0036` 2,723 of the 2,793 reachable nodes are more than 10 hops away, and the outage planner would report all of them as unaffected. Replacing the loop with `nx.descendants` is not equivalent either, because that ignores closed gates.

The only edit I made is a two-line comment above `seen = {start}` explaining why there is no depth limit, so the next reader does not have the same worry. Behaviour and tests are unchanged.
