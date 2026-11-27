# ADR 0007: routing currency conversions

Decision: in-process-library

160 currencies, ~2,300 pairs quoted both ways, cache refreshed every 10 s. Treasury: at most three conversions
(two intermediates), best rate, never through a restricted currency. 300/s at peak, 15 ms budget. Graph in
memory with networkx; no graph database (Arjun's proposal rejected: a network hop for a graph this small).
