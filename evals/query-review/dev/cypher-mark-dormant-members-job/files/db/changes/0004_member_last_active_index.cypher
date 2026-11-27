CREATE INDEX member_last_active IF NOT EXISTS FOR (m:Member) ON (m.lastActiveAt);
