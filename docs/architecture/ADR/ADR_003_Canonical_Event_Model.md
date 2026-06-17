# ADR-003 Canonical Event Model

Status: Accepted

Date: 2026

---

## Context

The platform will ingest data from:

* ForexFactory
* Investing.com
* Reuters
* Bloomberg
* NewsAPI
* Future Sources

Each source has a different structure.

---

## Decision

All sources must publish a single canonical event contract.

Refer:

02_Event_Contract.md

No downstream service shall depend on source-specific fields.

---

## Consequences

Benefits:

* Source interchangeability
* Validation reuse
* Persistence reuse
* Monitoring reuse

Trade-offs:

* Additional normalization effort

Decision Approved.
