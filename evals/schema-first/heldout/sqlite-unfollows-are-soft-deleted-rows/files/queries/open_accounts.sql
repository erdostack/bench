SELECT COUNT(*) AS open_accounts
FROM account
WHERE deleted_at IS NULL;
