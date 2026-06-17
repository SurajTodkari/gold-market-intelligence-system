from datetime import datetime, UTC


def create_trace(event_id):

    return {

        "event_id": event_id,

        "created_at":
        datetime.now(UTC),

        "stages": []
    }


def add_stage(trace, stage_name):

    trace["stages"].append({

        "stage": stage_name,

        "timestamp":
        datetime.now(UTC)
    })

    return trace