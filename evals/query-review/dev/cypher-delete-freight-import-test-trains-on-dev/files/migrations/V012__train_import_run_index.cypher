// V012: clean-ups and comparisons filter on importRun.
CREATE INDEX train_import_run IF NOT EXISTS FOR (t:Train) ON (t.importRun);
