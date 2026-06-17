from monitoring.metrics.postgres_metrics import (

    increment_metric,

    get_metric,

    get_all_metrics,

    reset_metrics
)


class MetricsCollector:

    # -------------------------------
    # Increment Metric
    # -------------------------------

    def increment(

        self,

        metric_name
    ):

        increment_metric(

            metric_name
        )

    # -------------------------------
    # Get Metric
    # -------------------------------

    def get_metric(

        self,

        metric_name
    ):

        return get_metric(

            metric_name
        )

    # -------------------------------
    # Get All Metrics
    # -------------------------------

    def get_all_metrics(self):

        return get_all_metrics()

    # -------------------------------
    # Reset Metrics
    # -------------------------------

    def reset(self):

        reset_metrics()


# -----------------------------------
# Singleton Instance
# -----------------------------------

metrics_collector = MetricsCollector()