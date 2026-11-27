# Capacity snapshot, 2026-11-10

| | |
|---|---|
| accounts | 44.1 million rows |
| entities | 97.6 million rows |
| links | 318.2 million rows; 61 GB table, 74 GB of indexes |
| links growth | about 9 million rows a month |
| link writes | 1,100 inserts or `last_seen` updates per second at peak, from the event consumer |
| accounts per entity | p50 1, p99 14, max 1.9 million (carrier NAT address) |
| entities per account | p50 3, p99 210 |
| replicas | 4, each 32 vCPU and 128 GB memory; replication lag under 1 s |
| service pods | 24, each 4 GB memory |

`shared_buffers` is 32 GB on each replica. The links table and its indexes do not fit in memory; the
buffer cache hit rate for `links` and `links_entity_account_idx` is 91%.
