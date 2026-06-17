from monitoring.metrics.metrics_collector import (
    metrics_collector
)

from monitoring.alerts.alert_rules import (

    MAX_FAILED_EVENTS,

    MAX_DLQ_EVENTS,

    MAX_DUPLICATE_EVENTS,

    MIN_EVENTS_PERSISTED
)

from shared.logging.logger import app_logger


# -----------------------------------
# Alert Evaluation
# -----------------------------------

def evaluate_alerts():

    metrics = (

        metrics_collector
        .get_all_metrics()
    )

    alerts = []

    # -------------------------
    # Failed Events Alert
    # -------------------------

    if metrics.get(

        "events_failed",

        0

    ) > MAX_FAILED_EVENTS:

        alerts.append(

            "ALERT: High Validation Failure Rate"
        )

    # -------------------------
    # DLQ Alert
    # -------------------------

    if metrics.get(

        "dlq_events",

        0

    ) > MAX_DLQ_EVENTS:

        alerts.append(

            "ALERT: DLQ Growth Detected"
        )

    # -------------------------
    # Duplicate Alert
    # -------------------------

    if metrics.get(

        "duplicate_events",

        0

    ) > MAX_DUPLICATE_EVENTS:

        alerts.append(

            "WARNING: High Duplicate Event Volume"
        )

    # -------------------------
    # Persistence Alert
    # -------------------------

    if metrics.get(

        "events_persisted",

        0

    ) < MIN_EVENTS_PERSISTED:

        alerts.append(

            "WARNING: No Events Persisted"
        )

    return alerts


# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    alerts = evaluate_alerts()

    if alerts:

        for alert in alerts:

            app_logger.warning(

                alert
            )

    else:

        app_logger.info(

            "No Active Alerts"
        )