# Release Checklist

Release: v1.1.0-multi-source-ingestion

---

Pre-Release

[ ] Code reviewed

[ ] Unit tests passed

[ ] Integration tests passed

[ ] Kafka verified

[ ] Validation verified

[ ] Persistence verified

[ ] Metrics verified

[ ] Tracing verified

[ ] Documentation updated

---

Release

[ ] Merge to main

[ ] Create tag

git tag -a v1.1.0-multi-source-ingestion -m "Investing.com adapter release"

[ ] Push tag

git push origin v1.1.0-multi-source-ingestion

---

Post Release

[ ] Grafana healthy

[ ] Prometheus healthy

[ ] Kafka healthy

[ ] PostgreSQL healthy

[ ] No DLQ spike detected

[ ] Release notes published
