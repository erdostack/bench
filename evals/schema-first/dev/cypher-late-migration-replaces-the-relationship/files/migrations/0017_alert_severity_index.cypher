CREATE INDEX alert_severity IF NOT EXISTS FOR (a:Alert) ON (a.severity);
