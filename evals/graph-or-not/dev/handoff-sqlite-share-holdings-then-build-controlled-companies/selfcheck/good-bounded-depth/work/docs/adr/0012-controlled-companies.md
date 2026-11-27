# 0012. Controlled companies: where the walk runs

Status: Accepted, 2026-11-23

Decision: recursive-sql

Context, as given by the product owner: compliance (Sigrid) defines control for the client page panel as 25% or
more of the shares at every step. 2.1M companies and 3.4M holdings; chains are at most 9 companies long; about
1,100 holdings close a loop and the registry feed allows that. 2,500 page views a day, 2 s for the panel. A
recursive query measured 140 ms on a replica for the largest group.

Rejected: a graph database (Neha), an in-memory copy in the web app. Neither buys anything at 140 ms of 2 s.

Revisit if the panel misses 2 s.
