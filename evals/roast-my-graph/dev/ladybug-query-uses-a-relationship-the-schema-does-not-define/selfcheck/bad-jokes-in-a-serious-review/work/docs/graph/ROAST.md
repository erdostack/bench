# Review: shelfmates queries

Release sign-off, serious faces on. One of these queries did not read the schema and it is about to be embarrassed in front of everyone.

## Findings

### 1. genre_top (critical)

**Problem.** This query strides confidently into the schema and asks for Reviewed, a relationship that has never existed outside its own imagination. The schema has Rated. Reviewed is the friend it made up to seem interesting. Every other query got the memo.

**Fix.** Swap Reviewed for Rated in genre_top: (b:Book)<-[x:Rated]-(r:Reader). Then it can stop talking to people who are not there.

Signed off, pending one imaginary friend.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
