from validation.schema_validation.schema_validator import validate_event

from datetime import datetime , UTC


event = {

    "event_id": "evt_001",

    "source": "ForexFactory",

    "event_type": "CPI_RELEASE",

    "country": "US",

    "title": "US CPI Data Released",

    "published_at": datetime.now(UTC),

    "ingested_at": datetime.now(UTC),

    "payload": {
        "actual": "3.4",
        "forecast": "3.2"
    }
}

validated = validate_event(event)

print(validated)