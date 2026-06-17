from sqlalchemy import text

from storage.postgres.db import SessionLocal

from shared.logging.logger import app_logger


def get_postgres_status():

    db = SessionLocal()

    try:

        result = db.execute(

            text(
                "SELECT COUNT(*) FROM market_events"
            )
        )

        row_count = result.scalar()

        return {

            "status": "UP",

            "market_events_count":
                row_count
        }

    except Exception as e:

        app_logger.error(

            f"Postgres Monitor Error | "
            f"{e}"
        )

        return {

            "status": "DOWN",

            "error": str(e)
        }

    finally:

        db.close()


if __name__ == "__main__":

    report = get_postgres_status()

    app_logger.info(

        f"Postgres Monitor Report | "
        f"{report}"
    )