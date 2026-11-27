WITH RECURSIVE
  formula_ref AS (SELECT src_sheet, src_addr, dst_sheet, dst_addr FROM ref WHERE kind = 'formula'),
  hit(s, a) AS (
    VALUES (:sheet, :addr)
    UNION
    SELECT f.src_sheet, f.src_addr FROM formula_ref f JOIN hit h ON f.dst_sheet = h.s AND f.dst_addr = h.a
  )
SELECT s AS sheet, a AS addr FROM hit;
