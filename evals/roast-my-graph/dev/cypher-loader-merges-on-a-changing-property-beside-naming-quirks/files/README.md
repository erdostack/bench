# postroom

Audience graph for a paid-newsletter platform. Neo4j 5.

    graph/schema.cypher    constraints and indexes
    graph/load.cypher      nightly load from the billing export (the loader passes `$rows` in batches of 5,000)
    graph/queries.cypher   what the dashboards run; each query has a `// name:` line

## How it is fed

Billing is the source of truth. Every night the loader gets the full export (every subscriber, every
subscription, yesterday's opens) and replays it through `load.cypher`, top to bottom. A subscriber's row
carries the plan they are on that night: `free`, `monthly`, `annual` or `comp`. About 3% of subscribers change
plan in a month.

## What reads it

- `audience_size` is the number shown to advertisers, and the number they are invoiced on.
- `plan_mix` and `issue_opens` feed each writer's dashboard.
- `subscriber_card` is the support tool's lookup.

## Size

| Thing | Count |
|---|---|
| `Subscriber` | 2.4 million |
| `Newsletter` | 5,800 |
| `Issue` | 410,000 |
| `SUBSCRIBED_TO` | 6.1 million |
| `OPENED` | 90 days kept, about 300 million |
