# ADR-002 Kafka Transport

Status: Accepted

Date: 2026

---

## Context

The system requires:

* Reliable event delivery
* Replay capability
* Scalability
* Service independence

---

## Decision

Apache Kafka shall be the primary transport mechanism between services.

Topics:

topic.raw.ingestion

topic.validated.events

topic.deadletter.validation

topic.deadletter.persistence

---

## Consequences

Benefits:

* Replay support
* High throughput
* Durable messaging
* Service decoupling

Trade-offs:

* Additional infrastructure
* Operational monitoring requirements

Decision Approved.
