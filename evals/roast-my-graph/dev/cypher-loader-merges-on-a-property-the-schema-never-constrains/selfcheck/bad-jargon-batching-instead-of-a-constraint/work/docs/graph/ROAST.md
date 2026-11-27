# Roast: galleria graph

An eager pipeline meets a transaction log.

## Findings

### 1. load_artworks (high)

**Problem.** The UNWIND/MERGE pipeline is executed as one eager transaction per batch with four concurrent writers, causing lock contention and heap pressure on the transaction state. The existing uniqueness constraint on Artwork already gives MERGE its index-backed lookup.

**Fix.** Wrap the load in CALL { ... } IN TRANSACTIONS OF 500 ROWS, reduce the workers to one, and raise the page cache.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
