# Review

The CL204 warnings are reasonable hygiene; adding directions removes the risk of duplicates.

## neighbours.cypher (medium)

Bidirectional traversal (CL204) risks duplicate rows depending on how relationships were loaded.

Fix: Specify direction for determinism.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
