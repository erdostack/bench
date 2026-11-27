Added sql/no_shows.sql: speakers with at least one session starting on :event_day and no speaker_checkin row on that
day, one row per speaker (speaker_id, name). Dates are compared with date() on both timestamps.
