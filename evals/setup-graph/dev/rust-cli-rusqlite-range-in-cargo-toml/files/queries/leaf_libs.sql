SELECT t.label FROM target AS t
WHERE t.kind = 'lib' AND NOT EXISTS (SELECT 1 FROM needs AS n WHERE n.a = t.label)
ORDER BY t.label;
