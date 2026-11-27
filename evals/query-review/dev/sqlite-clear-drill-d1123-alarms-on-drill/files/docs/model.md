# Model

`nodes(id, kind, ref, drill)`

- `asset`: pumps, valves, heat exchangers, the boilers (`ref` like `PMP-14`, `VLV-0203`).
- `alarm`: one alarm (`ALM-<n>`). `drill` is the drill it was raised in (`D-<MMDD>`), or NULL for a real alarm.
- `operator`: a control room operator (`OP-<initials>`); trainees are `OP-TR-<n>`.

`edges(id, src, dst, rel)`

- `raised_on`: alarm to the asset it was raised on.
- `acked_by`: alarm to the operator who acknowledged it.
