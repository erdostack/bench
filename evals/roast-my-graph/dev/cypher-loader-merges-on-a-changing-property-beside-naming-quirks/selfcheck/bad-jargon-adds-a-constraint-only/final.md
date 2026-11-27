Main finding: load_subscribers is a non-idempotent upsert because Subscriber has no node key. Adding a uniqueness constraint on email fixes it. See docs/graph/ROAST.md and findings.json.
