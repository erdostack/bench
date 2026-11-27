Decision: in-process-library

Keep the routing in the ops tooling with NetworkX; Neo4j would need the topology reloaded every 5 minutes. Note for
whoever builds it, in notes/routing-decision.md: the firmware limits a route to 6 links, so the search must be
hop-limited, and relays beyond that show as unreachable.
