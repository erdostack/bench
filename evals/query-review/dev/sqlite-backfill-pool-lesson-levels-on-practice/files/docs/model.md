# Model

`nodes.kind`: `pool` (`POOL-WYF`), `lesson`, `swimmer` (`SW-...`), `instructor` (`IN-...`).

Lesson codes are `LS-<pool>-<day>-<time>-<stage>`, for example `LS-WYF-SAT-0930-S3`. The stage is `S1` to
`S7` for the learn-to-swim stages; adult and aquafit lessons end in `AD` or `AQ` instead and have no level.

`nodes.level` is the stage a lesson teaches. When a group moves up a stage mid-term the instructor changes
`level` and the code stays as it was, so where `level` is set it is right even if the code says otherwise.
