# Review

The totals are inflated because the loader creates duplicate relationships in both directions.

## collaboration_total (high)

Inflated counts from duplicate COAUTHORED relationships: MERGE on a directed pattern creates a second edge when the pair arrives reversed (bidirectional duplication).

Fix: Deduplicate with apoc.refactor.mergeRelationships and switch the loader to an undirected MERGE.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
