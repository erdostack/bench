-- transfers are in xfr; fee per club
SELECT c.full_nm AS club, SUM(x.fee_k) AS euros_paid
FROM xfr x JOIN clb c ON c.clb_id = x.src_clb
GROUP BY c.clb_id, c.full_nm
ORDER BY euros_paid DESC;
