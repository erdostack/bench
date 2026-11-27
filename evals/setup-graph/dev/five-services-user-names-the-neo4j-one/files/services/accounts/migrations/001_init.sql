CREATE TABLE customer (id serial PRIMARY KEY, name text NOT NULL, parent_id integer REFERENCES customer(id));
CREATE TABLE contract (id serial PRIMARY KEY, customer_id integer NOT NULL REFERENCES customer(id), starts_on date NOT NULL);
CREATE TABLE invoice (id serial PRIMARY KEY, customer_id integer NOT NULL REFERENCES customer(id), issued_on date NOT NULL, total_cents bigint NOT NULL);
