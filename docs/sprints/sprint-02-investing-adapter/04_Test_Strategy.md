# Test Strategy

Sprint: Investing.com Adapter

---

# Unit Tests

Validate:

* Event extraction
* Parser logic
* Canonical mapping

---

# Integration Tests

Validate:

Investing.com
→ Kafka
→ Validation
→ Persistence

---

# Contract Tests

Validate:

Canonical Event Contract compliance.

---

# Observability Tests

Validate:

Metrics exposed on:

http://localhost:8000/metrics

Validate:

* events_received
* events_validated
* events_persisted

---

# Tracing Tests

Validate:

SCRAPER
→ VALIDATION
→ PERSISTENCE

trace chain exists.

---

# Failure Tests

Kafka unavailable

Expected:
Retry framework activates.

---

Database unavailable

Expected:
DLQ path activated.

---

DOM structure changes

Expected:
Parser failure logged.
