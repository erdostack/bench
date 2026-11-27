// 0081: country codes to upper case (a few imports wrote 'de', 'fr').
MATCH (s:Site) WHERE s.country <> toUpper(s.country)
CALL (s) {
  SET s.country = toUpper(s.country)
} IN TRANSACTIONS OF 5000 ROWS;
