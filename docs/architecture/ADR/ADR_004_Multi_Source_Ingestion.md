# ADR-004 Multi Source Ingestion

Status: Accepted

Date: 2026

---

## Context

Relying on a single source introduces:

* Availability risk
* Data quality risk
* Vendor dependency

---

## Decision

The platform shall support multiple independent sources.

Initial Sources:

* ForexFactory
* Investing.com

Future Sources:

* Reuters
* Bloomberg
* NewsAPI
* TradingEconomics

---

## Consequences

Benefits:

* Improved resilience
* Cross-source validation
* Confidence scoring foundation
* Reduced vendor dependency

Trade-offs:

* Increased ingestion complexity
* Source reconciliation requirements

Decision Approved.
