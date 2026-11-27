// why: wallet screen filters on expiry. Reviewed: s.okonkwo.
CREATE INDEX offer_expires IF NOT EXISTS FOR (o:Offer) ON (o.expires);
