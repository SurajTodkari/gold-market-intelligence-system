from kafka import KafkaConsumer
from kafka.errors import KafkaError

from sqlalchemy import text

from storage.postgres.db import SessionLocal

from monitoring.metrics.metrics_collector import (
    metrics_collector
)

from shared.logging.logger import app_logger


# -----------------------------------
# Kafka Health Check
# -----------------------------------

def check_kafka():

    try:

        consumer = KafkaConsumer(

            bootstrap_servers="127.0.0.1:9092",

            api_version_auto_timeout_ms=5000
        )

        consumer.close()

        return True

    except KafkaError as e:

        app_logger.error(

            f"Kafka Health Check Failed | "
            f"{e}"
        )

        return False


# -----------------------------------
# PostgreSQL Health Check
# -----------------------------------

def check_postgres():

    db = SessionLocal()

    try:

        db.execute(

            text("SELECT 1")
        )

        return True

    except Exception as e:

        app_logger.error(

            f"PostgreSQL Health Check Failed | "
            f"{e}"
        )

        return False

    finally:

        db.close()


# -----------------------------------
# Metrics Health Check
# -----------------------------------

def check_metrics():

    try:

        metrics = (

            metrics_collector
            .get_all_metrics()
        )

        return metrics

    except Exception as e:

        app_logger.error(

            f"Metrics Health Check Failed | "
            f"{e}"
        )

        return {}


# -----------------------------------
# Overall Health Report
# -----------------------------------

def generate_health_report():

    report = {

        "kafka": check_kafka(),

        "postgres": check_postgres(),

        "metrics": check_metrics()
    }

    return report


# -----------------------------------
# Standalone Execution
# -----------------------------------

if __name__ == "__main__":

    report = generate_health_report()

    app_logger.info(

        f"System Health Report | "
        f"{report}"
    )