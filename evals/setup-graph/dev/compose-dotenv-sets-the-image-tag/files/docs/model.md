# Model

- `(:Buoy {code, depth_m})` and `(:Station {code})`.
- `(:Buoy)-[:RELAYS_TO {range_km}]->(:Buoy|:Station)`: the direction readings travel.

A buoy with one outgoing RELAYS_TO is a single point of failure for everything upstream of it.
