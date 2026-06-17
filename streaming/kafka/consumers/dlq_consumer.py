from kafka import KafkaConsumer
from shared.logging.logger import app_logger
import json

consumer = KafkaConsumer(

    "topic.deadletter.persistence",

    bootstrap_servers="127.0.0.1:9092",

    auto_offset_reset="earliest",

    group_id="dlq-consumer",

    value_deserializer=lambda x:
    json.loads(x.decode("utf-8"))
)

#app_logger.warning(

 #   f"DLQ Event Received: "
  #  f"{message.value}"
#)

for message in consumer:

    app_logger.warning(

        f"DLQ Event Received: "
        f"{message.value}"
    )

    print("\nDLQ EVENT RECEIVED:\n")

    print(

        json.dumps(

            message.value,

            indent=4
        )
    )