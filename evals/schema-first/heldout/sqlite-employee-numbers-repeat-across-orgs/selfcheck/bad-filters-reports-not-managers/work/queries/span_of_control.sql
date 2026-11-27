SELECT m.name AS manager, COUNT(*) AS direct_reports
FROM staff e
JOIN staff m ON e.mgr_no = m.emp_no
WHERE e.org = 'lumen'
GROUP BY m.org, m.emp_no, m.name
ORDER BY direct_reports DESC;
