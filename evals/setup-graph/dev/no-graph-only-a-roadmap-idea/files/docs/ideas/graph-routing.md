# Idea: route suggestions on a graph

Status: idea, not started. Nothing in the codebase depends on this.

Today a parcel's route is whatever the dispatcher types in. If hubs were nodes and scheduled runs were
relationships, "cheapest way from hub A to hub B before Friday" would be one query, roughly:

    MATCH p = SHORTEST 1 (a:Hub {code: $from})-[:RUN]->+(b:Hub {code: $to})
    RETURN p

Open points before anyone builds this: who keeps the run schedule up to date, whether the data is big enough to
need a separate database at all, and hosting.
