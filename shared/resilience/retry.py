from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from shared.logging.logger import app_logger


def resilient_retry():

    return retry(

        stop=stop_after_attempt(5),

        wait=wait_exponential(

            multiplier=2,

            min=2,

            max=30
        ),

        retry=retry_if_exception_type(Exception),

        before_sleep=lambda state:
        app_logger.warning(
            f"Retrying after error: "
            f"{state.outcome.exception()}"
        ),

        reraise=True
    )