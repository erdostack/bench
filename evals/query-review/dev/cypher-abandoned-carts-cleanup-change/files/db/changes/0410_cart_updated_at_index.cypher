CREATE INDEX cart_updated_at IF NOT EXISTS FOR (c:Cart) ON (c.updatedAt);
