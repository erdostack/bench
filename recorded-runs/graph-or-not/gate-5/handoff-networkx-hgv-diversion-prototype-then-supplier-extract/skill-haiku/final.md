Decision: in-process-library

With the regional extract at 180,000 segments and 150,000 junctions, the diversion checker can hold the network in one worker. That is about 332 MB at the pilot's per-segment cost, against the 1.5 GB limit, and a measured check on a synthetic network of that size had a median of about 0.9 s against the 2 s budget. The earlier need-more-information call turned on the regional count, which is now known and under the 800,000-segment bound I recorded.

The decision rests on the arithmetic and on a synthetic measurement, not the real extract. The edge scan, which runs over every segment before each route search, is most of the check time, so it is the first thing to fix if the real figures are slower. Before go-live, load the real extract into one worker and time real checks and traced memory.

Updated: `docs/graph/DECISION.md`, with the old values kept beside the new ones where the count changed. Nothing else in the repo was changed.

Numbers the call turns on:
- Regional memory: 180,000 x 1,842 B = about 332 MB (derived from the pilot's 70 MB over 38,000 segments). A measured synthetic load was 245 MB, so either figure leaves most of the 1.5 GB free.
- Measured check time, synthetic grid: median 889 ms and maximum 1,212 ms at 180,000 segments, with 805 ms of the median in the edge scan. A second run gave a median of 998 ms and a maximum of 1,449 ms.
- The pilot's reported 30 ms per route is far below the 172 ms I measured at pilot size on this machine, and I could not reconcile the two.

Still open: the real extract's attributes and route mix, the real memory and timing, the number of worker copies and the reload cadence, and whether the platform can host a graph database service. Owners of the limits are noted in the decision file.
