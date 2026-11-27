# Model

```
(:Site {siteId, kind})                 kind: 'hub' | 'cell' | 'core'
(:Site)-[:BACKHAUL {medium, capacityKbps, since}]->(:Site)
```

One BACKHAUL relationship per link (about 410,000), pointing from the site nearer the core to the
other; traffic flows both ways. `capacityKbps` is an INTEGER.
