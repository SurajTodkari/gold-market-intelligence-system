from kafka import KafkaConsumer
from kafka.errors import KafkaError

import json
from datetime import datetime

from streaming.kafka.producers.dlq_producer import send_to_dlq

from monitoring.tracing.request_tracer import (
    add_stage
)

from monitoring.tracing.trace_manager import (
    log_trace
)

from monitoring.metrics.metrics_collector import (
    metrics_collector
)

from shared.logging.logger import app_logger
from shared.resilience.retry import resilient_retry

from storage.postgres.db import SessionLocal
from storage.postgres.models.event_model import MarketEvent


# -----------------------------------
# Kafka Consumer Configuration
# -----------------------------------

consumer = KafkaConsumer(

    "topic.validated.events",

    bootstrap_servers="127.0.0.1:9092",

    auto_offset_reset="latest",

    enable_auto_commit=True,

    group_id="persistence-group-v3",

    value_deserializer=lambda x:
    json.loads(x.decode("utf-8"))
)


# -----------------------------------
# Database Session
# -----------------------------------

db = SessionLocal()


# -----------------------------------
# Service Metrics
# -----------------------------------

processed_events = 0
failed_events = 0


# -----------------------------------
# Retry Protected Save Function
# -----------------------------------

@resilient_retry()
def save_event(db, market_event):

    db.add(market_event)

    db.flush()

    db.commit()

    return True


# -----------------------------------
# Service Startup
# -----------------------------------

app_logger.info(
    "Persistence Service Started..."
)

app_logger.info(
    "Metrics Collector Connected"
)

# -----------------------------------
# Consume Kafka Events
# -----------------------------------

try:

    for message in consumer:

        event = None

        try:

            event = message.value

            app_logger.info(

                f"Received Event From Kafka | "
                f"Event={event.get('event_name')}"
            )

            # -----------------------------------
            # Parse Timestamps
            # -----------------------------------

            published_at = datetime.fromisoformat(
                event["published_at"]
            )

            ingested_at = datetime.fromisoformat(
                event["ingested_at"]
            )

            # -----------------------------------
            # Create ORM Object
            # -----------------------------------

            market_event = MarketEvent(

                source_event_id=
                event["source_event_id"],

                source=
                event["source"],

                event_name=
                event["event_name"],

                country=
                event["country"],

                currency=
                event["currency"],

                impact=
                event["impact"],

                actual=
                event["actual"],

                forecast=
                event["forecast"],

                previous=
                event["previous"],

                source_event_date=
                event["source_event_date"],

                source_event_time=
                event["source_event_time"],

                published_at=
                published_at,

                ingested_at=
                ingested_at
            )

            # -----------------------------------
            # Save To Database
            # -----------------------------------
            if "trace" in event:          #before saving to database, we are adding the stage to the trace which is coming from the previous stages and then we will log the trace for monitoring purposes

                add_stage(
                event["trace"],
               "PERSISTENCE"
            )
                

            save_event(
                db,
                market_event
            )

            processed_events += 1

            metrics_collector.increment(
               "events_persisted"
            )

            if "trace" in event:

                log_trace(
                event["trace"]
               )
                

            app_logger.info(

                f"Saved Event To PostgreSQL | "
                f"Source Event ID={event['source_event_id']} | "
                f"Event={event['event_name']}"
            )

        except KafkaError as ke:

            failed_events += 1

            metrics_collector.increment(
                "events_failed"
            )

            app_logger.error(

                f"Kafka Processing Error | "
                f"Error={ke}"
            )

        except Exception as e:

            failed_events += 1

            metrics_collector.increment(
                 "events_failed"
            )

            metrics_collector.increment(
                 "dlq_events"
            )

            db.rollback()

            send_to_dlq(
                event if event else {},
                str(e)
            )

            app_logger.error(

                f"Database Persistence Error | "
                f"Event={event.get('event_name') if event else 'UNKNOWN'} | "
                f"Error={e}"
            )

            app_logger.warning(
                "Event routed to DLQ"
            )

        

except KeyboardInterrupt:

    app_logger.warning(
        "Persistence Service Stopped Manually"
    )

except Exception as e:

    app_logger.error(

        f"Fatal Persistence Service Error | "
        f"Error={e}"
    )

finally:

    db.close()

    app_logger.info(

        f"Persistence Service Summary | "
        f"Processed={processed_events} | "
        f"Failed={failed_events}"
    )

    app_logger.info(
        "Database Session Closed"
    )