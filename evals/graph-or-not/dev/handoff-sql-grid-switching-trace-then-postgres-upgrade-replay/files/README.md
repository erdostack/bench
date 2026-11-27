# outage-trace

Answers the control room's question "which customers lose supply if this device opens?" for the distribution
network. The network model lives in the `netmodel` Postgres database, loaded from the GIS and updated by the
switching feed (SCADA) as devices change state.

- `trace/service.py`: HTTP endpoint the control-room client calls.
- `sql/outage_trace.sql`: the trace.
- `db/schema.sql`: the tables the trace reads.
