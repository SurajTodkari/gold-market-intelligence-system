from pydantic import BaseModel

from datetime import datetime


class MarketEvent(BaseModel):

    source_event_id: str

    source: str

    event_name: str

    country: str

    currency: str

    impact: str

    actual: str

    forecast: str

    previous: str

    source_event_date: str

    source_event_time: str

    published_at: datetime

    ingested_at: datetime