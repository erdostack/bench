// Works filed under $subject or any narrower subject.
MATCH (top:Subject {label: $subject})<-[:BROADER*0..10]-(s:Subject)<-[:ABOUT]-(w:Work)
RETURN DISTINCT w.title AS title, w.first_published AS first_published, s.label AS filed_under
ORDER BY title
LIMIT toInteger($limit)
