CREATE INDEX build_finished IF NOT EXISTS FOR (b:Build) ON (b.finishedAt);
