SELECT u.login, COUNT(*) AS issues
FROM issue i
JOIN usr u ON u.usr_id = i.assignee
WHERE i.state <> 'closed'
GROUP BY u.login;
