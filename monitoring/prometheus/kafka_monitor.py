from kafka import KafkaConsumer

from shared.logging.logger import app_logger


def get_kafka_status():

    try:

        consumer = KafkaConsumer(

            bootstrap_servers="127.0.0.1:9092",

            api_version_auto_timeout_ms=5000
        )

        topics = consumer.topics()

        consumer.close()

        return {

            "status": "UP",

            "topics": list(topics)
        }

    except Exception as e:

        app_logger.error(

            f"Kafka Monitor Error | "
            f"{e}"
        )

        return {

            "status": "DOWN",

            "error": str(e)
        }


if __name__ == "__main__":

    report = get_kafka_status()

    app_logger.info(

        f"Kafka Monitor Report | "
        f"{report}"
    )