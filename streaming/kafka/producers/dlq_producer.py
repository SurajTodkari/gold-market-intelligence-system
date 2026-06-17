from kafka import KafkaProducer
import json

DLQ_TOPIC = "topic.deadletter.persistence"

producer = KafkaProducer(

    bootstrap_servers="127.0.0.1:9092",

    value_serializer=lambda v:
    json.dumps(v, default=str).encode("utf-8")
)


def send_to_dlq(event, error_message):

    dlq_event = {

        "failed_event": event,

        "error": error_message
    }

    producer.send(

        DLQ_TOPIC,

        dlq_event
    )

    producer.flush()