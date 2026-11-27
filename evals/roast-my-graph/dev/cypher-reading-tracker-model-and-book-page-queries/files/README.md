# shelfmates

A reading tracker: people shelve books, rate them and follow each other. Neo4j 5.26.

    model/model.md          labels and relationships
    model/schema.cypher     constraints
    queries/book.cypher     book page
    queries/reader.cypher   reader profile and rating

## Sizes

900,000 readers, 1.4 million books, 18 million ratings (a reader rates a book at most once; rating
again replaces the stars), 40 million SHELVED.

## Book page

About 250 views a second. Shows the average stars (`book_stars`) and "readers who loved this also
loved" (`loved_also_loved`, from 4 and 5 star ratings).
