Decision: in-process-library

You've measured both relational routes and they miss the 1 s budget by a wide margin (14 s and 6.5 s p95), while
the networkx prototype does it in 0.18 s on 3.4 GB of a 16 GB host.

- The depth is the problem: the pairs people ask about are a median of 4 links apart and 31% need 5 or more, and a
  breadth-first frontier over 9.6M links explodes past 3.
- A day stale is fine and links change ~20k a day, so a nightly rebuild from the dump is enough.
- A graph database would also work, but it is another store to operate and feed when the graph fits in memory with
  room to spare at 25 requests a second.
