# Review: shelfmates queries

Scope: the six queries in store/queries.cypher, each checked name by name against the tables in store/schema.cypher. One query does not match the schema. Five do.

## Findings

### 1. genre_top (critical)

**Problem.** The query walks from Book to Reader over a relationship called Reviewed. schema.cypher defines no such thing. The only relationship from Reader to Book is Rated, which is what shelf, book_rating and friends_liked all use and where `stars` lives. As written, genre_top refers to a table that does not exist, so the Discover tab's genre list cannot return results.

**Fix.** Use the relationship that exists: MATCH (g:Genre)<-[:InGenre]-(b:Book)<-[x:Rated]-(r:Reader) WHERE g.slug = $slug RETURN b.isbn, b.title, avg(x.stars) AS score, count(x) AS votes ORDER BY score DESC LIMIT 20. Consider requiring a minimum number of votes so a single five-star rating does not top the list.

### 2. book_rating (low)

**Problem.** Recomputes the average over all of a book's ratings on each page view.

**Fix.** Acceptable at 2.6 million ratings. If a few books collect very many ratings, store score and votes on Book and update them when a rating is written.

shelf, book_page, book_rating, friends_liked and follower_count use only tables, columns and directions that the schema defines.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
