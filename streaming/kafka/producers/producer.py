from kafka import KafkaProducer
from kafka.errors import KafkaError

from shared.logging.logger import app_logger
from shared.resilience.retry import resilient_retry

import json


# -----------------------------------
# Kafka Configuration
# -----------------------------------

KAFKA_TOPIC = "topic.raw.ingestion"


producer = KafkaProducer(

    bootstrap_servers="127.0.0.1:9092",

    value_serializer=lambda v:
    json.dumps(v, default=str).encode("utf-8"),

    retries=5,

    acks="all"
)


# -----------------------------------
# Publish Event
# -----------------------------------

@resilient_retry()
def publish_event(event):

    future = producer.send(

        KAFKA_TOPIC,

        event
    )

    record_metadata = future.get(timeout=10)

    app_logger.info(

        f"Event Published | "
        f"Topic={record_metadata.topic} | "
        f"Partition={record_metadata.partition} | "
        f"Offset={record_metadata.offset}"
    )

    producer.flush()


# -----------------------------------
# Test Event
# -----------------------------------

event = {

    "event_type": "CPI_RELEASE",

    "country": "US",

    "actual": "3.4",

    "forecast": "3.2"
}


# -----------------------------------
# Main
# -----------------------------------

try:

    publish_event(event)

    app_logger.info(
        "Producer completed successfully"
    )

except KafkaError as e:

    app_logger.error(
        f"Kafka Error: {e}"
    )

except Exception as e:

    app_logger.error(
        f"Producer Error: {e}"
    )