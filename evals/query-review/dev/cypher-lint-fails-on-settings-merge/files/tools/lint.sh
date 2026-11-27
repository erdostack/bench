#!/bin/sh
# CI entry point; graphlint is installed in the CI image only.
exec graphlint --config .graphlint.yml
