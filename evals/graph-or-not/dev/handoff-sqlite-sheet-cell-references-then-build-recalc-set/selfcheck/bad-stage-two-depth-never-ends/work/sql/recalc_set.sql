WITH RECURSIVE downstream(sheet, addr, depth) AS (
    SELECT src_sheet, src_addr, 1 FROM ref
    WHERE dst_sheet = :sheet AND dst_addr = :addr AND kind = 'formula'
  UNION ALL
    SELECT r.src_sheet, r.src_addr, d.depth + 1
    FROM ref AS r JOIN downstream AS d ON r.dst_sheet = d.sheet AND r.dst_addr = d.addr
    WHERE r.kind = 'formula'
)
SELECT DISTINCT sheet, addr FROM downstream;
