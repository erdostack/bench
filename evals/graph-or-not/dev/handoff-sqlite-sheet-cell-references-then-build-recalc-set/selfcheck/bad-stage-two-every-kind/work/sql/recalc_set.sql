-- Cells to recalculate after (:sheet, :addr) is edited: everything that reads it through formula
-- references of any kind. UNION on (sheet, addr) with no depth column, so circular references end.
WITH RECURSIVE downstream(sheet, addr) AS (
    SELECT src_sheet, src_addr
    FROM ref
    WHERE dst_sheet = :sheet AND dst_addr = :addr
  UNION
    SELECT r.src_sheet, r.src_addr
    FROM ref AS r
    JOIN downstream AS d ON r.dst_sheet = d.sheet AND r.dst_addr = d.addr
)
SELECT sheet, addr
FROM downstream
WHERE NOT (sheet = :sheet AND addr = :addr)
ORDER BY sheet, addr;
