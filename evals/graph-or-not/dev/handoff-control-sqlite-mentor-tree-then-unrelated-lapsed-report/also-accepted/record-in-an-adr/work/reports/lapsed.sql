-- Active volunteers with no shift in the 90 days up to and including :as_of (never-worked volunteers included).
SELECT v.id, v.name
FROM volunteer v
WHERE v.active = 1
  AND NOT EXISTS (
      SELECT 1 FROM shift s
      WHERE s.volunteer_id = v.id
        AND s.shift_date > date(:as_of, '-90 days')
        AND s.shift_date <= :as_of
  )
ORDER BY v.name;
