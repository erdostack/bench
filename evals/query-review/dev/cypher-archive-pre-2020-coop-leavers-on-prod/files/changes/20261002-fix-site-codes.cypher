// 20261002: Brook Farm's site code was entered as 'BF ' (trailing space) when the site was added; fix it.
// Reviewed: h.lund. Run on prod 2026-10-02.
MATCH (s:Site {code: 'BF '}) SET s.code = 'BF';
