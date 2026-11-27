// name: shelf
MATCH (r:Reader)-[x:Rated]->(b:Book)
WHERE r.id = $reader
RETURN b.isbn, b.title, x.stars, x.rated_on
ORDER BY x.rated_on DESC
LIMIT 100;

// name: book_page
MATCH (b:Book)
WHERE b.isbn = $isbn
RETURN b.title, b.year;

// name: book_rating
MATCH (r:Reader)-[x:Rated]->(b:Book)
WHERE b.isbn = $isbn
RETURN avg(x.stars) AS score, count(x) AS votes;

// name: friends_liked
MATCH (me:Reader)-[:Follows]->(f:Reader)-[x:Rated]->(b:Book)
WHERE me.id = $reader AND x.stars >= 4
RETURN b.isbn, b.title, count(f) AS friends
ORDER BY friends DESC
LIMIT 20;

// name: genre_top
MATCH (g:Genre)<-[:InGenre]-(b:Book)<-[x:Reviewed]-(r:Reader)
WHERE g.slug = $slug
RETURN b.isbn, b.title, avg(x.stars) AS score, count(x) AS votes
ORDER BY score DESC
LIMIT 20;

// name: follower_count
MATCH (r:Reader)<-[:Follows]-(f:Reader)
WHERE r.id = $reader
RETURN count(f) AS followers;
