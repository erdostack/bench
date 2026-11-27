Added a unique index on (contributor, title, kind, role) and ON CONFLICT DO NOTHING, so the 1,000 already written are skipped and self-translators keep both roles.
