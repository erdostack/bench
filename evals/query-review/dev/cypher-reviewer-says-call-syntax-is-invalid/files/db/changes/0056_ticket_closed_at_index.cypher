CREATE INDEX ticket_closed_at IF NOT EXISTS FOR (t:Ticket) ON (t.closedAt);
