# ADR 0001: where the route report runs

Status: accepted

Decision: in-process-library

Context, from the owner: about 2,300 relays and 14,000 links in production; the controller republishes the
topology every 5 minutes; on-call runs the report about 40 times a day. The relay firmware drops a message after
6 hops, so a route may use at most 6 links, and a relay only reachable in more hops counts as unreachable.

NetworkX on the ops box (already installed, relay/topology.py already loads the GraphML). A graph database
(the network team's wish) would need a reimport every 5 minutes for a computation that takes milliseconds.
