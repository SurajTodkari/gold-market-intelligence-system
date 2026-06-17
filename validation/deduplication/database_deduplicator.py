from storage.postgres.db import SessionLocal
from storage.postgres.models.event_model import MarketEvent


def event_exists(source_event_id: str) -> bool:

    db = SessionLocal()

    try:

        existing = (

            db.query(MarketEvent)

            .filter(

                MarketEvent.source_event_id
                == source_event_id

            )

            .first()
        )

        return existing is not None

    finally:

        db.close()