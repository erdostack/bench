# Changelog

## 0.8.0
- sqlite-jdbc pinned back in build.sbt: the newer native library would not load on the greenhouse
  terminal (old glibc). Revisit when the terminal is replaced.
- New report: label coverage per bed.

## 0.7.0
- Lineage query returns the propagation method at every step.
