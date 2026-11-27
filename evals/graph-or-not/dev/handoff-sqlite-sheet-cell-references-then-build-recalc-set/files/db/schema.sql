-- One workbook per SQLite file on the doc server.
CREATE TABLE sheet (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE cell (
  sheet   TEXT NOT NULL,     -- sheet name
  addr    TEXT NOT NULL,     -- A1 style
  formula TEXT,              -- NULL for a plain value
  value   TEXT,              -- last computed or typed value
  PRIMARY KEY (sheet, addr)
);

-- Every reference in the workbook. src reads dst: the formula in src, or a chart, data validation rule or
-- conditional format anchored at src, uses the value of dst.
CREATE TABLE ref (
  src_sheet TEXT NOT NULL,
  src_addr  TEXT NOT NULL,
  dst_sheet TEXT NOT NULL,
  dst_addr  TEXT NOT NULL,
  kind      TEXT NOT NULL CHECK (kind IN ('formula', 'chart', 'validation', 'cond_format'))
);

CREATE INDEX ref_by_dst ON ref (dst_sheet, dst_addr);
CREATE INDEX ref_by_src ON ref (src_sheet, src_addr);
