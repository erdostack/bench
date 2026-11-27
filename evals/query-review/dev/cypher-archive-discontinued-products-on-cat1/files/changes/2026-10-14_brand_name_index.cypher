// change: index Brand.name for the brand pages. Reviewed: j.mwangi.
CREATE INDEX brand_name IF NOT EXISTS FOR (b:Brand) ON (b.name);
