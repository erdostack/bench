select speaker_id, name from speaker join session_speaker on speaker_id = speaker.id
join session on session.id = session_id
where substr(starts_at, 1, 10) = :event_day
except
select speaker_id, speaker.name from speaker_checkin join speaker on speaker.id = speaker_id
where substr(checked_in_at, 1, 10) = :event_day
