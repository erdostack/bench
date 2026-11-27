# Review

All three undirected queries double count. Add directions everywhere.

## collaboration_total.cypher (high)

Undirected pattern doubles the counts.

Fix: Add a direction.

## cross_faculty_links.cypher (high)

Undirected pattern doubles the counts.

Fix: Add a direction.

## my_coauthors.cypher (high)

Undirected pattern returns each coauthor twice.

Fix: Add a direction.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
