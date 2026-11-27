The job selected every gis2009 pipe, so the retry would have multiplied the 7,000 pipes the crashed
run had already converted a second time. It now selects only gis2009 rows still in inches (under
50, since the smallest converted size is 50.8 mm), in chunks of 1,000, so tonight's run converts the
remaining 24,000 and any later run finds nothing to do. Check: `SELECT count(*) FROM pipe WHERE
source = 'gis2009' AND diameter < 50` should be 0 afterwards.
