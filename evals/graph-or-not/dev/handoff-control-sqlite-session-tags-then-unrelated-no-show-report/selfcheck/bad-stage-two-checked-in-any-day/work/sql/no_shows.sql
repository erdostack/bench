SELECT DISTINCT sp.id, sp.name
FROM speaker sp
JOIN session_speaker ss ON ss.speaker_id = sp.id
JOIN session s ON s.id = ss.session_id
WHERE date(s.starts_at) = :event_day
  AND sp.id NOT IN (SELECT speaker_id FROM speaker_checkin);
