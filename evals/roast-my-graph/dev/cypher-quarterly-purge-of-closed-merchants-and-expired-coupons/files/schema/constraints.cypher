CREATE CONSTRAINT merchant_id IF NOT EXISTS FOR (m:Merchant) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT card_token IF NOT EXISTS FOR (c:Card) REQUIRE c.token IS UNIQUE;
CREATE CONSTRAINT coupon_code IF NOT EXISTS FOR (c:Coupon) REQUIRE c.code IS UNIQUE;
CREATE INDEX merchant_closed_on IF NOT EXISTS FOR (m:Merchant) ON (m.closed_on);
CREATE INDEX coupon_expires_on IF NOT EXISTS FOR (c:Coupon) ON (c.expires_on);
