SELECT v.id, v.name
FROM volunteer v
JOIN shift s ON s.volunteer_id = v.id
WHERE v.active = 1
GROUP BY v.id, v.name
HAVING MAX(s.shift_date) <= date(:as_of, '-90 days')
ORDER BY v.name;
