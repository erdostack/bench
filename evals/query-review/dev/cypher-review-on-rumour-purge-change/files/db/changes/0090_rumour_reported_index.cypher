CREATE INDEX rumour_reported IF NOT EXISTS FOR ()-[r:RUMOURED_TO]-() ON (r.reportedAt);
