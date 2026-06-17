from shared.logging.logger import app_logger


VALID_IMPACTS = {

    "LOW",
    "MEDIUM",
    "HIGH"
}


def validate_integrity(event):

    try:

        # -----------------------------
        # Required Fields
        # -----------------------------

        required_fields = [

            "source_event_id",
            "event_name",
            "country",
            "currency",
            "impact"
        ]

        for field in required_fields:

            if not event.get(field):

                app_logger.warning(

                    f"Integrity Check Failed | "
                    f"Missing Field={field}"
                )

                return False

        # -----------------------------
        # Impact Validation
        # -----------------------------

        if (

            event["impact"]

            not in VALID_IMPACTS

        ):

            app_logger.warning(

                f"Integrity Check Failed | "
                f"Invalid Impact="
                f"{event['impact']}"
            )

            return False

        # -----------------------------
        # Currency Validation
        # -----------------------------

        if len(

            event["currency"]

        ) != 3:

            app_logger.warning(

                f"Integrity Check Failed | "
                f"Invalid Currency="
                f"{event['currency']}"
            )

            return False

        return True

    except Exception as e:

        app_logger.error(

            f"Integrity Validation Error | "
            f"{e}"
        )

        return False