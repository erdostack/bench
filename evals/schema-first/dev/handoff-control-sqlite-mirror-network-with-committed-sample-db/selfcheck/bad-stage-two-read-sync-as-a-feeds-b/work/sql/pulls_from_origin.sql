-- sync(a, b): a -> b
SELECT m.host
FROM sync s
JOIN mirror m ON m.mirror_id = s.b
JOIN mirror o ON o.mirror_id = s.a
WHERE o.host = 'origin.pkgs.example.org';
