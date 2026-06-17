from storage.postgres.db import engine

from monitoring.metrics.metrics_model import (
    SystemMetric
)

from storage.postgres.models.event_model import Base


Base.metadata.create_all(bind=engine)

print("Tables created successfully!")