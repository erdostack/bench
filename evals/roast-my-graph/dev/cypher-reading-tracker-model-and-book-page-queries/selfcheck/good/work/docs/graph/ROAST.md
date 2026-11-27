# Roast: shelfmates model and queries

The main model change: Rating should be a relationship, not a node. It only ever links one reader
to one book and carries stars and a date, so it costs you an extra hop on every rating query,
including the book page's also-loved list. Make it RATED {stars, rated_at} from Reader to Book.
Details in docs/graph/ROAST.md and findings.json.

## Findings

### 1. Rating (medium)

**Problem.** A Rating connects exactly one reader to exactly one book and nothing else ever attaches to it; it just holds stars and a date. That makes it a relationship stored as a node: 18 million extra nodes, and every query that uses ratings walks two hops instead of one. loved_also_loved on the book page walks four hops where two would do.

**Fix.** Model it as (:Reader)-[:RATED {stars, rated_at}]->(:Book). rate becomes MATCH both, MERGE (u)-[r:RATED]->(b) SET r.stars = $stars, r.rated_at = datetime(); loved_also_loved becomes (b)<-[r1:RATED]-(u)-[r2:RATED]->(other).

### 2. loved_also_loved (medium)

**Problem.** For a very popular book this reads every 4-5 star reader's ratings on each page view.

**Fix.** Precompute the list nightly for books with many ratings.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
