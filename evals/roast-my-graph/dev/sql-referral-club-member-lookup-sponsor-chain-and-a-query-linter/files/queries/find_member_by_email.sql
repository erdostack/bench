SELECT id, name FROM member WHERE lower(email) = lower($1);
