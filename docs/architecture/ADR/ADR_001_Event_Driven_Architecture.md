# ADR-001 Event Driven Architecture

Status: Accepted

Date: 2026

---

## Context

The Gold Market Intelligence System must support:

* Multiple data sources
* Independent services
* Scalability
* Fault tolerance
* Future intelligence modules

Traditional tightly coupled architectures create bottlenecks and reduce scalability.

---

## Decision

The platform shall adopt an Event Driven Architecture.

All system interactions occur through events.

Services communicate through Kafka topics.

---

## Consequences

Benefits:

* Loose coupling
* Independent deployment
* Horizontal scalability
* Easier testing
* Better fault isolation

Trade-offs:

* Increased operational complexity
* Kafka dependency

Decision Approved.
