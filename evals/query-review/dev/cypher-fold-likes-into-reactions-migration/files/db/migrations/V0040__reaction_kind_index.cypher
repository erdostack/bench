CREATE INDEX reacted_kind IF NOT EXISTS FOR ()-[r:REACTED]-() ON (r.kind);
