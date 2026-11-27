// name: articles_with_tag
MATCH (a:Article)-[:TaggedWith]->(t:Tag)
WHERE t.slug = $tag
RETURN a.id, a.title, a.section, a.published
ORDER BY a.published DESC
LIMIT 200;

// name: episodes_with_tag
MATCH (e:Episode)-[:TaggedWith]->(t:Tag)
WHERE t.slug = $tag
RETURN e.id, e.title, e.show, e.published
ORDER BY e.published DESC
LIMIT 200;

// name: articles_by_person
MATCH (a:Article)-[m:MadeBy]->(p:Person)
WHERE p.staff_no = $staff_no
RETURN a.id, a.title, m.credit, a.published
ORDER BY a.published DESC
LIMIT 200;

// name: episodes_by_person
MATCH (e:Episode)-[m:MadeBy]->(p:Person)
WHERE p.staff_no = $staff_no
RETURN e.id, e.title, m.credit, e.published
ORDER BY e.published DESC
LIMIT 200;

// name: article_tags
MATCH (a:Article)-[:TaggedWith]->(t:Tag)
WHERE a.id = $id
RETURN t.slug, t.label, t.kind
ORDER BY t.kind, t.label;

// name: related_tags
// tags that appear on the same articles as this one
MATCH (t:Tag)<-[:TaggedWith]-(a:Article)-[:TaggedWith]->(other:Tag)
WHERE t.slug = $tag AND other.slug <> $tag
RETURN other.slug, other.label, count(*) AS together
ORDER BY together DESC
LIMIT 30;

// name: article_by_slug
MATCH (a:Article)
WHERE a.slug = $slug
RETURN a.id, a.title, a.published;
