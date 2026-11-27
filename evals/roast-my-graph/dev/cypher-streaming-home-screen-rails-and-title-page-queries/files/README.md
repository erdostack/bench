# reelhouse

Catalogue graph for the streaming app, Neo4j 5.26.

    model/model.md          labels and relationships
    model/schema.cypher     constraints
    queries/home.cypher     home screen rails
    queries/title.cypher    title page

## Sizes

| Thing | Count |
|---|---|
| Title | 48,000 (31,000 available in our region) |
| Genre | 46 |
| IN_GENRE | a title has 1 to 4 genres, about 105,000 in all; the largest genre has 9,000 titles |
| Viewer | 6.2 million |
| FAVOURS | 3 to 8 genres per viewer, picked at sign-up |
| WATCHED | 1.9 billion; median viewer 310 titles |

## Who calls what

- Home screen, on every open: `continue_watching`, `watch_next` ("Picked for you"), and one
  `genre_rail` per genre shelf.
- `genre_rail` is the same for everyone, so the CDN caches each rail for an hour: it runs 46 times an
  hour in total.
- Title page: `title_page`.
