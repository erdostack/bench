The one that matters: load_subscribers matches on email and plan together, so every plan change leaves the old subscriber in place and creates a second one. Both get the subscriptions and the opens, and audience_size (what advertisers pay on) counts them twice. Fix is to match on email alone and set the plan after, then delete the copies. Rated critical.

The odd names (partOf, SentAt) are only odd; they are consistent everywhere, so low.

Everything is in docs/graph/ROAST.md and findings.json.
