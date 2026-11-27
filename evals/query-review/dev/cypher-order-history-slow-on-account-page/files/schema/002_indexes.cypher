CREATE INDEX customer_email IF NOT EXISTS FOR (c:Customer) ON (c.email);
