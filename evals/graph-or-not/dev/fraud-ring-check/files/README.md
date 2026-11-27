# riskgate

Synchronous risk checks called by the payment gateway while a card authorisation is in flight. The
gateway gives us 250 ms in total. If we do not answer in time the payment is approved without our
verdict.

Checks: velocity, device reputation, sanctions list, and the **ring check** (is this account linked,
through shared devices, cards or addresses, to an account already confirmed as fraud).

    db/        schema and migrations (PostgreSQL 15, one primary and four read replicas)
    sql/       the queries the service runs
    ops/       exports from monitoring
    docs/adr/  decision records
    tickets/   open tickets, exported

The service is Go, 24 pods, 4 GB memory each, stateless.
