from datetime import datetime


def validate_timestamp(event_time):

    try:

        if event_time is None:

            print("Timestamp missing")

            return False

        if not isinstance(event_time, datetime):

            print("Invalid timestamp type")

            return False

        return True

    except Exception as e:

        print(f"Timestamp validation failed: {e}")

        return False