Added sql/payer.sql. It walks account_link upwards following only kind = 'legal' and returns the last account it
reaches, or the account itself when it has no legal parent. That is the rule recorded in docs/adr/0007-paying-account-for-consolidated.md:
the legal chain decides who pays, parent_account_id (the old CRM import) and the finance links do not. Recursive SQL
as decided; tested on SQLite built from db/schema.sql.
