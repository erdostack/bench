CREATE NODE TABLE School(code STRING PRIMARY KEY, name STRING);
CREATE NODE TABLE PriceList(code STRING PRIMARY KEY, name STRING);
CREATE NODE TABLE Product(sku STRING PRIMARY KEY, name STRING, size_range STRING);

CREATE REL TABLE UsesList(FROM School TO PriceList, MANY_ONE);
CREATE REL TABLE PricedOn(FROM Product TO PriceList, price_cents INT64, valid_from DATE, valid_to DATE);
