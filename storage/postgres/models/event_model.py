from sqlalchemy import (
    Column,
    String,
    DateTime
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MarketEvent(Base):

    __tablename__ = "market_events"

    source_event_id = Column(
        String,
        primary_key=True
    )

    source = Column(String)

    event_name = Column(String)

    country = Column(String)

    currency = Column(String)

    impact = Column(String)

    actual = Column(String)

    forecast = Column(String)

    previous = Column(String)

    source_event_date = Column(String)

    source_event_time = Column(String)

    published_at = Column(DateTime)

    ingested_at = Column(DateTime)