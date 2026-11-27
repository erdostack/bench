# Custom procedures

`parcel.handoffs(from, to, maxLegs)` returns the cheapest chain of depots between two depots, counting
a fixed cost per hand-off. It is a server-side procedure because the cost model needs every leg's
timetable, which is too much to ship to the client.

Built and tested against Neo4j 5.26.24. The jar is copied into the server image's `/plugins` by the
Dockerfile; there is nothing to install by hand.
