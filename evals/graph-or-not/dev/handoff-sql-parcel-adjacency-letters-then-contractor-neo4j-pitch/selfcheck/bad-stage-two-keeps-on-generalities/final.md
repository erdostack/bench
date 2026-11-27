Position: keep

Thanks. We decided to keep this as a join on parcel_adjacency in Postgres (no-graph). The adjacency is already
computed by the GIS team, a second database adds operational cost and a sync job, and neighbour lookups on an
indexed table are fast. We don't see a need for a graph database here.
