# RISK-881: payments approved without a ring verdict

**Opened by:** risk operations · **Priority:** high · **Status:** open

On 2026-11-10 the ring check returned no verdict for 96,880 authorisations (4.2% of the day's
2,310,400). Those payments were approved on the other checks alone. In October, 212 chargebacks later
confirmed as ring fraud were on payments where the ring check had been cancelled.

Two more things from our side:

1. **Depth.** Since April the authorisation path only looks 4 steps out. In the rings we confirmed last
   quarter, the nearest already-known fraud account was 5 or 6 steps away in 31% of cases. We only
   find those in the review queue, and the 6-step query there is cancelled at its 120 s limit 38% of
   the time (6,916 of 18,200 runs yesterday).

2. **Freshness.** Someone suggested computing groups overnight. For mule accounts confirmed last
   quarter, the median time from account creation to first cash-out was 40 minutes. A link that is
   visible tomorrow morning is not useful.

---

**Halima (risk engineering), 2026-11-11**

We have asked for a graph database twice. Can someone who is not us look at the numbers?
