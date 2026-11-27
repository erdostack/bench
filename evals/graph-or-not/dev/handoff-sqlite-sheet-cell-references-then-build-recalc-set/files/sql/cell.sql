-- The stored formula and value of one cell. :sheet, :addr
SELECT formula, value
FROM cell
WHERE sheet = :sheet AND addr = :addr;
