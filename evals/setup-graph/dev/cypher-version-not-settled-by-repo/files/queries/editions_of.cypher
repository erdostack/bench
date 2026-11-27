// Editions of a work, newest first, with the language of each.
MATCH (w:Work {title: $title})-[:HAS_EDITION]->(e:Edition)
RETURN e.isbn AS isbn, e.year AS year, e.language AS language
ORDER BY year DESC
