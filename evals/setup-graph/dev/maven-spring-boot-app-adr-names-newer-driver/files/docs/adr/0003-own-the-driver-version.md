# ADR 0003: Pin the driver in our pom

Status: Accepted (2026-02-11)

The driver version is declared in our own dependencyManagement (property `graph-driver.version`), so
it no longer changes when the Spring Boot parent is bumped.
