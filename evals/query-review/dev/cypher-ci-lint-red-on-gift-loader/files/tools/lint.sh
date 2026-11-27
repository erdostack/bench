#!/bin/sh
# CI entry point: lints every Cypher file with the repo configuration.
exec cypherlint --config .cypherlint.yml
