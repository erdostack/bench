# Scores shown in the product

Both are computed nightly from the follower export and must be reproducible: the same export gives the same
numbers.

## Reach

PageRank over follows, rank passing from the follower to the account they follow.

- N is the number of accounts in `accounts.txt`, including accounts that follow nobody and have no followers.
- Every account starts at 1/N.
- One step: reach(v) = (1 - d)/N + d * sum over followers u of v of reach(u)/following(u), plus d/N times the total
  reach of the accounts u with following(u) = 0. following(u) is the number of accounts u follows; an account with
  following(u) = 0 passes its reach to nobody, so it is spread over all N accounts instead.
- d = 0.85. Exactly 20 steps, no convergence test, so that numbers stay comparable from night to night.

## Ring

Accounts joined by a chain of follows, in either direction, are in the same ring. Every account has a ring id;
the id itself means nothing, only which accounts share one.
