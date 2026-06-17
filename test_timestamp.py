from datetime import datetime, UTC, timedelta

from validation.timestamp_validation.timestamp_validator import validate_timestamp


fresh_time = datetime.now(UTC)

old_time = datetime.now(UTC) - timedelta(minutes=10)


print(validate_timestamp(fresh_time))

print(validate_timestamp(old_time))