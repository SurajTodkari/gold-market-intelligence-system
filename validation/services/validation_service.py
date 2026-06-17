from kafka import KafkaConsumer
from kafka import KafkaProducer

import json

from monitoring.tracing.request_tracer import (
    add_stage
)

from shared.logging.logger import app_logger

from monitoring.metrics.metrics_collector import (
    metrics_collector
)

from validation.integrity_checks.integrity_validator import (
    validate_integrity
)

from validation.deduplication.database_deduplicator import (
    event_exists
)

from shared.config.topics import (
    RAW_TOPIC,
    VALIDATED_TOPIC,
    DLQ_TOPIC
)

from validation.schema_validation.schema_validator import (
    validate_event
)

from validation.timestamp_validation.timestamp_validator import (
    validate_timestamp
)


# -----------------------------------
# Kafka Consumer
# -----------------------------------

consumer = KafkaConsumer(

    RAW_TOPIC,

    bootstrap_servers="127.0.0.1:9092",

    auto_offset_reset="latest",

    group_id="validation-group-v3",

    value_deserializer=lambda x:
    json.loads(x.decode("utf-8"))
)


# -----------------------------------
# Kafka Producer
# -----------------------------------

producer = KafkaProducer(

    bootstrap_servers="127.0.0.1:9092",

    value_serializer=lambda v:
    json.dumps(v, default=str).encode("utf-8")
)


# -----------------------------------
# Service Startup
# -----------------------------------

app_logger.info(
    "Validation Service Started..."
)

app_logger.info(
    "Metrics Collector Connected"
)


# -----------------------------------
# Main Loop
# -----------------------------------

for message in consumer:

    event = message.value

    metrics_collector.increment(
        "events_received"
    )

    try:

        # -------------------------
        # Schema Validation
        # -------------------------

        validated = validate_event(event)

        if validated is None:

            raise Exception(
                "Schema validation failed"
            )

        # -------------------------
        # Integrity Validation
        # -------------------------

        if not validate_integrity(event):

            raise Exception(
                "Integrity validation failed"
            )

        # -------------------------
        # Timestamp Validation
        # -------------------------

        if not validate_timestamp(

            validated.published_at

        ):

            raise Exception(
                "Timestamp validation failed"
            )

        # -------------------------
        # Database Deduplication
        # -------------------------

        if event_exists(

            validated.source_event_id

        ):

           metrics_collector.increment(
              "duplicate_events"
            )

           app_logger.info(

             f"Duplicate Event Skipped | "
             f"{validated.source_event_id}"
         )
  
           continue
        # -------------------------
        # Publish Validated Event
        # -------------------------
        if "trace" in event:  #Just added for the tracing 14-06-2026 at evening

          add_stage(
            event["trace"],
           "VALIDATION"
             )
          

        producer.send(

            VALIDATED_TOPIC,

            event
        )

        producer.flush()

        metrics_collector.increment(
            "events_validated"
        )

        app_logger.info(

            f"Validated Event | "
            f"{validated.event_name}"
        )

    except Exception as e:

        metrics_collector.increment(
            "events_failed"
        )

        dlq_event = {

            "event": event,

            "error": str(e)
        }

        producer.send(

            DLQ_TOPIC,

            dlq_event
        )

        producer.flush()

        app_logger.warning(

            f"Validation Failed | "
            f"{str(e)}"
        )