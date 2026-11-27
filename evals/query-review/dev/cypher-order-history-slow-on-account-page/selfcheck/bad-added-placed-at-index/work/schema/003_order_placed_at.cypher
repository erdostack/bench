CREATE INDEX order_placed_at IF NOT EXISTS FOR (o:Order) ON (o.placedAt);
