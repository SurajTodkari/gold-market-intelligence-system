from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime
)

from datetime import datetime, UTC

from storage.postgres.models.event_model import Base


class SystemMetric(Base):

    __tablename__ = "system_metrics"

    metric_name = Column(
        String,
        primary_key=True
    )

    metric_value = Column(
        Integer,
        default=0
    )

    updated_at = Column(
        DateTime,
        default=lambda:
        datetime.now(UTC)
    )