SELECT id, handle, display_name, bio
FROM account
WHERE lower(handle) = lower(:handle);
