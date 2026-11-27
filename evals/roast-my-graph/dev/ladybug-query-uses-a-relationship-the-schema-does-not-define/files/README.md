# shelfmates

Book ratings for a reading club app. The graph is a LadybugDB database file bundled with the API server.

- `store/schema.cypher`: table definitions (run once)
- `store/queries.cypher`: every query the API runs, named with `// name:`; the API passes parameters

About 30,000 readers, 210,000 books, 2.6 million ratings, 48 genres.

Endpoints: `shelf` and `book_page` on every screen; `friends_liked` and `genre_top` on the Discover tab;
`follower_count` on profiles.
