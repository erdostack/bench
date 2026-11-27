# Invoice owner

Decision: in-process-library

- Highest org from the org upwards with its own billing account gets the invoice; none: the org itself.
- 412 orgs point at deleted parents (FKs not enforced). The chain ends at the last existing org.
