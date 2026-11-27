SELECT id, name FROM person WHERE lower(email) = lower(:email);
