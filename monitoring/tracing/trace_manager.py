from shared.logging.logger import app_logger


def log_trace(trace):

    app_logger.info(

        f"TRACE | "
        f"Event={trace['event_id']} | "
        f"Stages={trace['stages']}"
    )