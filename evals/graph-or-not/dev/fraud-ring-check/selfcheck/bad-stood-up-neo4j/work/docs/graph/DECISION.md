# Ring check: can it stay on Postgres?

Decision: graph-database

Short answer: no. I looked for a tuning fix and the repo shows the obvious ones were already done.

## Workload facts

- 318.2 million links (61 GB plus 74 GB of indexes), growing 9 million a month, written at up to 1,100
  per second. It does not fit in the replicas' memory.
- The check runs about 2.3 million times a day, up to 4,100 a minute, inside a 250 ms budget.
- 96,880 checks a day (4.2%) are cancelled at the 400 ms timeout and the payment goes through without
  a verdict. Checks that need 4 steps average 371 ms.
- The business needs more depth, not less: in 31% of confirmed rings the nearest known fraud account
  was 5 or 6 steps away. The 6-step query averages 41 s and is cancelled 38% of the time.
- Links have to be visible within minutes: mule accounts cash out a median of 40 minutes after creation.

## Options considered

- Stay on the recursive query in Postgres and tune further: rejected, because ADR 0007 shows the tuning
  has been done. Both join directions are indexed, memory settings were raised with no effect, widely
  shared devices are already skipped (and lowering that cap further loses 22% of rings), replicas
  doubled throughput without changing per-query time, a precomputed two-step table was dropped at 6.4
  billion rows because it could not keep up with writes, and searching from both ends in the service
  was slower. After all of that 4.2% still time out at 4 steps and 6 steps is out of reach.
- Hold the links in the service's memory: rejected. 24 pods with 4 GB each cannot hold a 61 GB table,
  and every pod would have to apply 1,100 changes a second to stay current.
- Precompute groups overnight: rejected by the 40-minute cash-out window.
- A store built for following links many steps out under concurrent writes: chosen. It is a new system
  to run, which is a real cost; it should be sized on a trial with a copy of the links and the real
  6-step question before anyone commits.

## What would change the decision

- Risk accepting a 3-step limit (3-step checks average 214 ms and rarely time out).
- A trial showing the candidate store cannot answer the 6-step check inside 250 ms at 4,100 a minute
  with the widely shared devices present.
- The gateway budget growing to seconds, which would put the existing query back in play.
