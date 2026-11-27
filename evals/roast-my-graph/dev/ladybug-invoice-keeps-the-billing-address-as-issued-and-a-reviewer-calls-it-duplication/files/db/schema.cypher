CREATE NODE TABLE Customer(
    id INT64 PRIMARY KEY,
    name STRING,
    billing_address STRING,
    vat_number STRING,
    payment_terms_days INT64
);

CREATE NODE TABLE Product(
    code STRING PRIMARY KEY,
    name STRING,
    unit_price_cents INT64
);

CREATE NODE TABLE Invoice(
    number INT64 PRIMARY KEY,
    issued_on DATE,
    due_on DATE,
    bill_to_name STRING,
    bill_to_address STRING,
    vat_number STRING
);

CREATE REL TABLE BilledTo(FROM Invoice TO Customer);
CREATE REL TABLE HasLine(FROM Invoice TO Product, line_no INT64, description STRING, qty INT64,
                     unit_price_cents INT64);
