# Engineering Standards Handbook

Project: Gold Market Intelligence System

Version: 1.0

Status: Approved

Owner: Architecture Team

Applies To:
All engineers, contributors, contractors, and future team members.

---

# 1. Purpose

This document establishes mandatory engineering standards for the Gold Market Intelligence System.

The objective is to ensure:

* Consistency
* Maintainability
* Scalability
* Reliability
* Observability
* Team Productivity

Failure to follow these standards introduces technical debt and architectural drift.

---

# 2. Architectural Principles

All development must follow:

1. Event Driven Architecture
2. Canonical Event Contract
3. Source Agnostic Processing
4. Loose Coupling
5. High Cohesion
6. Observability First
7. Fault Tolerance
8. Security by Default

---

# 3. Repository Structure

Mandatory Structure

docs/
ingestion/
validation/
storage/
streaming/
monitoring/
shared/
tests/

No engineer may create arbitrary top-level folders without architecture approval.

---

# 4. Ownership Model

Engineer 1

Domain:
Data Acquisition

Responsible For:

ingestion/
api_collectors/
browser_collectors/
rss_collectors/
websocket_collectors/

---

Engineer 2

Domain:
Data Reliability

Responsible For:

validation/
storage/
shared/schemas/

---

Engineer 3

Domain:
Observability

Responsible For:

monitoring/
grafana/
prometheus/
alerts/
tracing/

---

# 5. Naming Standards

Files

snake_case.py

Examples

forexfactory_scraper.py

validation_service.py

persistence_service.py

---

Classes

PascalCase

Example

MarketEvent

MetricsCollector

TraceManager

---

Functions

snake_case

Example

validate_event()

publish_event()

save_event()

---

Constants

UPPER_CASE

Example

RAW_TOPIC

DLQ_TOPIC

MAX_RETRY_COUNT

---

# 6. Logging Standards

All logging must use:

shared.logging.logger

Allowed

app_logger.info()

app_logger.warning()

app_logger.error()

Prohibited

print()

except during temporary debugging.

Before merging, all print statements must be removed.

---

# 7. Retry Standards

All external interactions must use:

shared.resilience.retry

Examples

HTTP Calls

Kafka Publishing

Browser Navigation

Database Writes

---

# 8. Kafka Standards

All communication between services must occur through Kafka.

Direct service-to-service calls are prohibited.

Allowed

Scraper
→ Kafka
→ Validation
→ Kafka
→ Persistence

Not Allowed

Scraper
→ Persistence

---

# 9. Database Standards

Database writes only occur inside:

storage/

No ingestion component may write directly to PostgreSQL.

---

# 10. Event Standards

Every source must publish:

Canonical Event Contract

No source-specific schemas are allowed downstream.

Refer:

02_Event_Contract.md

---

# 11. Testing Standards

Every new module requires:

Unit Tests

Integration Tests

Pipeline Validation

Minimum Coverage Goals

Critical Components:
80%

Utility Components:
70%

---

# 12. Documentation Standards

Every new module must contain:

Purpose

Dependencies

Input

Output

Failure Modes

Owner

No undocumented production component is allowed.

---

# 13. Git Standards

Branch Naming

feature/<feature-name>

Examples

feature/investing-adapter

feature/news-intelligence

feature/signal-engine

---

Bug Fixes

bugfix/<issue>

Example

bugfix/kafka-reconnect

---

Hotfixes

hotfix/<issue>

Example

hotfix/production-crash

---

# 14. Pull Request Standards

PR must contain:

Purpose

Files Changed

Testing Evidence

Risk Assessment

Rollback Plan

No direct commits to main.

---

# 15. Release Standards

Every release requires:

Git Tag

Release Notes

Architecture Review

QA Sign-off

Release Example

v1.1.0-multi-source-ingestion

---

# 16. Security Standards

No credentials in source code.

Use:

.env

Future Vault Integration

No secrets in Git.

---

# 17. Monitoring Standards

Every production service must expose:

Metrics

Health Check

Tracing

Alerts

No service may be deployed without observability.

---

# 18. Definition of Done

A task is complete only if:

Code Complete

Tests Passing

Documentation Updated

Metrics Verified

Tracing Verified

GitHub Updated

Peer Reviewed

Merged

Anything less is considered Work In Progress.

---

# 19. Architectural Rule

The platform is not a collection of scripts.

The platform is a long-term market intelligence system.

Every implementation decision must preserve:

Scalability
Reliability
Maintainability
Extensibility
Observability

for future Intelligence, Feature, Signal, Risk, and Execution layers.
