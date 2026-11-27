You're not covered yet. The batching counts merchants, and every merchant brings all of its payments
into the same inner transaction: 10,000 merchants is hundreds of millions of relationships per batch,
and the README shows even one big merchant didn't fit in 1 GB. Delete the PAID relationships in their
own IN TRANSACTIONS batches first, then the merchants. The coupon purge is fine as it is.
