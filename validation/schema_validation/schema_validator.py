from shared.schemas.event_schema import MarketEvent


def validate_event(event_data):

    try:

        validated_event = MarketEvent(**event_data)

        return validated_event

    except Exception as e:

        print("Validation failed:", e)

        return None