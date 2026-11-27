# 2025-06-12: profile pods killed by the friend-graph cache

## What happened

To serve "mutual friends" counts faster, profile-service pods loaded the friend graph into memory at start-up
and kept it current from the change feed. The pods have 4 GB each. At about 300 million friendships the cache
outgrew the pods and they were OOM-killed in a rolling loop for 50 minutes.

## Outcome

Rolled back the same day; mutual friends went back to two indexed lookups on the replica.

Follow-up (platform review, 2025-07): holding the friend graph in our own processes is off the table. We will not
build or run a custom stateful graph service of our own; anything that needs the whole graph in memory has to be
a product we can buy support for.
