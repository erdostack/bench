One of the three warnings matters a great deal; the other two you can close.

line_ridership is wrong, not just slow. It finds the month's taps, then separately finds the stations on the line, and nothing ties a tap to a station, so each station is counted against every tap in the whole network. Every station on the line comes out with the identical figure (the network total). That is the number going to the transport board. Fix: match the tap AT the station, the way busiest_stations does.

same_line also lists two patterns side by side, but each is a lookup of one station by its unique code, so it is one row times one row. zone_pairs really does pair everything with everything, on purpose, and there are six zones.

Details in docs/graph/ROAST.md and findings.json.
