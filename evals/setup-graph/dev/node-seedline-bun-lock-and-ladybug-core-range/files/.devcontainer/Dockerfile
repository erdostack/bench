ARG BUN_VERSION=1.2
FROM oven/bun:${BUN_VERSION}-debian

RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*
