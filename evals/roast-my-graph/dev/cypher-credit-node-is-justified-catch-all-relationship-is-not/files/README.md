# reelbase

Film and television credits. Neo4j 5.

    model/schema.cypher    constraints
    model/load.cypher      how the importer writes the graph
    model/queries.cypher   queries behind the site's pages (`// name:` gives the page)

## What the site needs

- An award is given for one specific piece of work: a person's role on one production. "Best supporting
  actor" attaches to that performance, not to the person in general and not to the production as a whole.
- An acting credit points at the character played. "Who else has played this character" is one of the two
  most visited pages; "awards for this performance" is the other.
- A person can hold several credits on the same production (director and writer, or two characters).
- Family and representation pages: a person's spouse, siblings and parents, and who their agent is.

## Size

| Thing | Count |
|---|---|
| `Person` | 2.8 million |
| `Production` | 640,000 |
| `Credit` | 19 million |
| `Character` | 4.1 million |
| `Award` | 310,000 |
| `RELATED` | 9 million, of which 7.6 million have kind `frequent_collaborator` (generated weekly from shared credits); the rest are `spouse`, `sibling`, `parent` and `agent` |
