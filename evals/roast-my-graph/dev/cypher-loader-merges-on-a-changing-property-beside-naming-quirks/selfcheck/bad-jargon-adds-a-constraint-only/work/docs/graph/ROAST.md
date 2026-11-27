# Roast: postroom graph

An upsert that is not idempotent is just an insert with extra steps.

## Findings

### 1. load_subscribers (high)

**Problem.** Non-idempotent upsert: the MERGE uses a composite match key and the Subscriber label has no node key, so entity resolution is not guaranteed and duplicate entities can be materialised.

**Fix.** Add a uniqueness constraint: CREATE CONSTRAINT subscriber_email_unique FOR (s:Subscriber) REQUIRE s.email IS UNIQUE. With a node key in place the MERGE becomes idempotent.

### 2. partOf (low)

**Problem.** Naming convention drift.

**Fix.** Rename to PART_OF.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
