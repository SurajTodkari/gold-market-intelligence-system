from datetime import datetime, UTC

from storage.postgres.db import SessionLocal

from monitoring.metrics.metrics_model import (
    SystemMetric
)


def increment_metric(metric_name):

    db = SessionLocal()

    try:

        metric = (

            db.query(SystemMetric)

            .filter(
                SystemMetric.metric_name
                == metric_name
            )

            .first()
        )

        if metric:

            metric.metric_value += 1

            metric.updated_at = (
                datetime.now(UTC)
            )

        else:

            metric = SystemMetric(

                metric_name=metric_name,

                metric_value=1,

                updated_at=datetime.now(UTC)
            )

            db.add(metric)

        db.commit()

    finally:

        db.close()


def get_metric(metric_name):

    db = SessionLocal()

    try:

        metric = (

            db.query(SystemMetric)

            .filter(
                SystemMetric.metric_name
                == metric_name
            )

            .first()
        )

        if metric:

            return metric.metric_value

        return 0

    finally:

        db.close()


def get_all_metrics():

    db = SessionLocal()

    try:

        metrics = (

            db.query(SystemMetric)

            .all()
        )

        return {

            metric.metric_name:
            metric.metric_value

            for metric in metrics
        }

    finally:

        db.close()


def reset_metrics():

    db = SessionLocal()

    try:

        metrics = (

            db.query(SystemMetric)

            .all()
        )

        for metric in metrics:

            metric.metric_value = 0

            metric.updated_at = (
                datetime.now(UTC)
            )

        db.commit()

    finally:

        db.close()