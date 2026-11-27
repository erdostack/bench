CREATE INDEX order_placed IF NOT EXISTS FOR (o:Order) ON (o.placedAt);
